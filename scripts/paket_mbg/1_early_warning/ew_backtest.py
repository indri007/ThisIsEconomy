#!/usr/bin/env python3
"""
Backtest Sistem Peringatan Dini (Early Warning) Wacana MBG
==========================================================

Menguji apakah lonjakan rasa jijik (disgust) / sarkasme di platform X
MENDAHULUI kejadian nyata (keracunan, penangguhan SPPG, pengumuman anggaran).

Input
-----
1. tweets CSV (wajib), minimal kolom:
     created_at  : waktu cuitan (ISO 8601, contoh 2026-03-05 14:22:00+07:00)
     emotion     : label emosi (Anger/Disgust/Fear/Joy/Trust/Neutral/Sadness/Interest/Surprise
                   atau versi Indonesia: Marah/Jijik/Takut/Senang/Percaya/Netral/Sedih/Minat/Terkejut)
     sarcasm     : 0/1 (atau True/False, "Sarkasme"/"Non-Sarkasme")
   opsional:  aspect (A1/A2/A3 atau nama aspek), tweet_id

2. events CSV (wajib), kolom:
     event_time  : tanggal/waktu kejadian PERTAMA KALI diberitakan resmi
     event_type  : keracunan / penangguhan_sppg / anggaran / lainnya
     description : ringkasan
     source_url  : tautan berita/rilis (wajib diisi agar dapat diverifikasi reviewer)

3. edges CSV (opsional) untuk DPPTI lengkap, kolom: source, target, created_at

Output (folder --out)
------
  signals.csv          sinyal per periode (share jijik, sarkasme, percaya, NetValence, DPPTI, z-score)
  alerts.csv           periode yang memicu alarm (z-score > ambang)
  event_leadtime.csv   untuk tiap kejadian: apakah didahului alarm & berapa jam lead time
  metrics.csv          precision, recall, median lead time, dsb.
  xcorr.csv            korelasi silang sinyal vs kejadian pada berbagai lag
  granger.csv          uji Granger (apakah sinyal membantu memprediksi kejadian)
  placebo.csv          uji permutasi: recall nyata vs recall dengan tanggal kejadian diacak
  plot_signals.png     grafik sinyal + garis kejadian
  RINGKASAN.md         ringkasan siap dikutip ke naskah

Contoh
------
  python ew_backtest.py --tweets tweets_classified.csv --events events.csv --out hasil
  python ew_backtest.py --tweets t.csv --events e.csv --edges edges.csv --freq 12h --window 72
"""
import argparse
import os
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

EMO_MAP = {
    "anger": "anger", "marah": "anger",
    "disgust": "disgust", "jijik": "disgust",
    "fear": "fear", "takut": "fear",
    "joy": "joy", "senang": "joy",
    "trust": "trust", "percaya": "trust",
    "neutral": "neutral", "netral": "neutral",
    "sadness": "sadness", "sedih": "sadness",
    "interest": "interest", "minat": "interest",
    "surprise": "surprise", "terkejut": "surprise",
}
NEG = {"disgust", "anger", "fear", "sadness"}
POS = {"joy", "trust"}


# ---------------------------------------------------------------- load
def load_tweets(path, tz):
    df = pd.read_csv(path)
    need = {"created_at", "emotion", "sarcasm"}
    miss = need - set(df.columns)
    if miss:
        raise SystemExit(f"[tweets] kolom wajib hilang: {miss}")
    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce", utc=True).dt.tz_convert(tz)
    bad = df["created_at"].isna().sum()
    if bad:
        print(f"[tweets] {bad} baris tanpa waktu valid dibuang")
    df = df.dropna(subset=["created_at"])
    df["emotion"] = df["emotion"].astype(str).str.strip().str.lower().map(EMO_MAP)
    unk = df["emotion"].isna().sum()
    if unk:
        print(f"[tweets] {unk} baris dengan label emosi tak dikenal dibuang")
    df = df.dropna(subset=["emotion"])
    s = df["sarcasm"].astype(str).str.strip().str.lower()
    df["sarcasm"] = s.isin(["1", "true", "sarkasme", "sarcasm", "yes", "ya"]).astype(int)
    return df


def load_events(path, tz):
    ev = pd.read_csv(path)
    if "event_time" not in ev.columns:
        raise SystemExit("[events] kolom wajib 'event_time' tidak ada")
    ev["event_time"] = pd.to_datetime(ev["event_time"], errors="coerce")
    if ev["event_time"].dt.tz is None:
        ev["event_time"] = ev["event_time"].dt.tz_localize(tz)
    else:
        ev["event_time"] = ev["event_time"].dt.tz_convert(tz)
    ev = ev.dropna(subset=["event_time"])
    if "event_type" not in ev.columns:
        ev["event_type"] = "lainnya"
    if ev.get("source_url") is None or ev["source_url"].isna().any():
        print("[events] PERINGATAN: sebagian kejadian tanpa source_url — lengkapi sebelum dilaporkan di naskah")
    return ev.sort_values("event_time").reset_index(drop=True)


# ---------------------------------------------------------------- network per window (opsional)
def network_metrics(edges, freq, tz):
    import networkx as nx
    from networkx.algorithms.community import louvain_communities, modularity

    e = pd.read_csv(edges)
    e["created_at"] = pd.to_datetime(e["created_at"], errors="coerce", utc=True).dt.tz_convert(tz)
    e = e.dropna(subset=["created_at"])
    rows = []
    for t, g in e.groupby(pd.Grouper(key="created_at", freq=freq)):
        if len(g) < 3:
            rows.append({"period": t, "Q": np.nan, "R": np.nan})
            continue
        G = nx.DiGraph()
        G.add_edges_from(zip(g["source"], g["target"]))
        R = nx.reciprocity(G) if G.number_of_edges() else np.nan
        U = G.to_undirected()
        try:
            comms = louvain_communities(U, seed=42)
            Q = modularity(U, comms)
        except Exception:
            Q = np.nan
        rows.append({"period": t, "Q": Q, "R": R})
    return pd.DataFrame(rows).set_index("period")


# ---------------------------------------------------------------- signals
def build_signals(tw, freq, roll, net=None, w=(0.4, 0.2, 0.2, 0.2), min_n=5):
    tw = tw.copy()
    tw["is_disgust"] = (tw["emotion"] == "disgust").astype(int)
    tw["is_trust"] = (tw["emotion"] == "trust").astype(int)
    tw["is_neg"] = tw["emotion"].isin(NEG).astype(int)
    tw["is_pos"] = tw["emotion"].isin(POS).astype(int)
    g = tw.groupby(pd.Grouper(key="created_at", freq=freq))
    s = pd.DataFrame({
        "n": g.size(),
        "disgust": g["is_disgust"].sum(),
        "trust": g["is_trust"].sum(),
        "neg": g["is_neg"].sum(),
        "pos": g["is_pos"].sum(),
        "sarcasm": g["sarcasm"].sum(),
    }).fillna(0)
    s.index.name = "period"
    n = s["n"].replace(0, np.nan)
    s["share_disgust"] = s["disgust"] / n
    s["share_sarcasm"] = s["sarcasm"] / n
    s["share_trust"] = s["trust"] / n
    s["net_valence"] = (s["pos"] - s["neg"]) / n          # -1..1
    s["low_volume"] = s["n"] < min_n

    # DPPTI (Bagian 7.2 naskah). Tanpa data jaringan: komponen Q dan R dihilangkan dan bobot dinormalisasi ulang.
    trust_ratio = s["trust"] / (s["trust"] + s["disgust"] + 1e-9)
    nv01 = (s["net_valence"] + 1) / 2
    if net is not None:
        s = s.join(net, how="left")
        comp = w[0] * trust_ratio + w[1] * (1 - s["Q"]) + w[2] * s["R"] + w[3] * nv01
    else:
        ww = np.array([w[0], w[3]]) / (w[0] + w[3])
        comp = ww[0] * trust_ratio + ww[1] * nv01
    s["dppti"] = comp

    # Sinyal peringatan: gabungan disgust + sarkasme + volume (volume dalam log agar tidak mendominasi)
    s["log_n"] = np.log1p(s["n"])
    for col in ["share_disgust", "share_sarcasm", "log_n", "dppti"]:
        mu = s[col].shift(1).rolling(roll, min_periods=max(3, roll // 2)).mean()
        sd = s[col].shift(1).rolling(roll, min_periods=max(3, roll // 2)).std()
        s[f"z_{col}"] = (s[col] - mu) / sd.replace(0, np.nan)
    # DPPTI turun = buruk -> tanda dibalik
    s["ew_score"] = s[["z_share_disgust", "z_share_sarcasm", "z_log_n"]].mean(axis=1, skipna=True)
    if s["z_dppti"].notna().any():
        s["ew_score"] = (s["ew_score"] * 3 - s["z_dppti"].fillna(0)) / 4
    return s


# ---------------------------------------------------------------- evaluation
def evaluate(s, ev, thr, window_h, freq):
    alerts = s[(s["ew_score"] > thr) & (~s["low_volume"])].copy()
    alerts["alert_time"] = alerts.index
    win = pd.Timedelta(hours=window_h)
    step = pd.Timedelta(freq)

    rows = []
    for _, e in ev.iterrows():
        t = e["event_time"]
        # alarm dihitung pada AKHIR periode (sinyal baru diketahui setelah periode selesai)
        prior = alerts[(alerts.index + step <= t) & (alerts.index + step >= t - win)]
        lead = (t - (prior.index.min() + step)).total_seconds() / 3600 if len(prior) else np.nan
        rows.append({**e.to_dict(), "preceded_by_alert": int(len(prior) > 0),
                     "n_alerts_before": len(prior), "lead_time_hours": lead})
    lead_df = pd.DataFrame(rows)

    tp_alerts = 0
    for t in alerts.index:
        t_end = t + step
        if ((ev["event_time"] >= t_end) & (ev["event_time"] <= t_end + win)).any():
            tp_alerts += 1
    precision = tp_alerts / len(alerts) if len(alerts) else np.nan
    recall = lead_df["preceded_by_alert"].mean() if len(lead_df) else np.nan
    f1 = 2 * precision * recall / (precision + recall) if precision and recall else np.nan
    metrics = pd.DataFrame([{
        "periode_total": len(s), "periode_volume_rendah": int(s["low_volume"].sum()),
        "jumlah_alarm": len(alerts), "jumlah_kejadian": len(ev),
        "ambang_z": thr, "jendela_jam": window_h,
        "precision": precision, "recall": recall, "f1": f1,
        "median_lead_time_jam": lead_df["lead_time_hours"].median(),
        "mean_lead_time_jam": lead_df["lead_time_hours"].mean(),
    }])
    return alerts, lead_df, metrics


def event_series(s, ev):
    y = pd.Series(0, index=s.index)
    for t in ev["event_time"]:
        idx = s.index.searchsorted(t, side="right") - 1
        if 0 <= idx < len(y):
            y.iloc[idx] = 1
    return y


def xcorr(s, y, max_lag):
    out = []
    x = s["ew_score"].fillna(0)
    for lag in range(-max_lag, max_lag + 1):
        # lag > 0: sinyal pada t, kejadian pada t+lag  (sinyal MENDAHULUI)
        r = x.corr(y.shift(-lag))
        out.append({"lag_periode": lag, "korelasi": r})
    return pd.DataFrame(out)


def granger(s, y, max_lag):
    from statsmodels.tsa.stattools import grangercausalitytests
    d = pd.DataFrame({"event": y.values, "signal": s["ew_score"].fillna(0).values})
    if d["event"].sum() < 3 or len(d) < 4 * max_lag + 5:
        return pd.DataFrame([{"catatan": "data terlalu sedikit untuk uji Granger"}])
    import contextlib, io
    with contextlib.redirect_stdout(io.StringIO()):
        try:
            res = grangercausalitytests(d[["event", "signal"]], maxlag=max_lag, verbose=False)
        except TypeError:  # statsmodels >= 0.15 menghapus argumen verbose
            res = grangercausalitytests(d[["event", "signal"]], maxlag=max_lag)
    return pd.DataFrame([{"lag": L, "F": r[0]["ssr_ftest"][0], "p_value": r[0]["ssr_ftest"][1]}
                         for L, r in res.items()])


def placebo(s, ev, thr, window_h, freq, n_perm=1000, seed=42):
    """Acak tanggal kejadian dalam rentang data; bandingkan recall nyata vs acak."""
    rng = np.random.default_rng(seed)
    _, real, _ = evaluate(s, ev, thr, window_h, freq)
    real_recall = real["preceded_by_alert"].mean()
    lo, hi = s.index.min().value, (s.index.max() + pd.Timedelta(freq)).value
    rec = []
    for _ in range(n_perm):
        fake = ev.copy()
        fake["event_time"] = pd.to_datetime(rng.integers(lo, hi, len(ev))).tz_localize("UTC").tz_convert(s.index.tz)
        _, ld, _ = evaluate(s, fake, thr, window_h, freq)
        rec.append(ld["preceded_by_alert"].mean())
    rec = np.array(rec)
    p = (np.sum(rec >= real_recall) + 1) / (n_perm + 1)
    return pd.DataFrame([{"recall_nyata": real_recall, "recall_acak_rata2": rec.mean(),
                          "recall_acak_p95": np.percentile(rec, 95), "p_value_permutasi": p,
                          "n_permutasi": n_perm}])


def plot(s, ev, thr, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(3, 1, figsize=(11, 7), sharex=True)
    ax[0].bar(s.index, s["n"], width=0.8 * (s.index[1] - s.index[0]) if len(s) > 1 else 0.8, color="#888780")
    ax[0].set_ylabel("Jumlah cuitan")
    ax[1].plot(s.index, s["share_disgust"], label="Proporsi jijik", color="#993C1D")
    ax[1].plot(s.index, s["share_sarcasm"], label="Proporsi sarkasme", color="#534AB7")
    ax[1].set_ylabel("Proporsi")
    ax[1].legend(loc="upper left", fontsize=8)
    ax[2].plot(s.index, s["ew_score"], color="#0F6E56", label="Skor peringatan dini")
    ax[2].axhline(thr, ls="--", color="#5F5E5A", lw=1, label=f"Ambang z = {thr}")
    ax[2].set_ylabel("Skor (z)")
    ax[2].legend(loc="upper left", fontsize=8)
    for a in ax:
        for t in ev["event_time"]:
            a.axvline(t, color="#A32D2D", lw=0.8, alpha=0.6)
    ax[2].set_xlabel("Waktu (garis merah = kejadian resmi)")
    fig.tight_layout()
    fig.savefig(path, dpi=200)


def fmt(x, d=2):
    return "—" if pd.isna(x) else f"{x:.{d}f}".replace(".", ",")


def summary(metrics, xc, gr, pl, args, path):
    m = metrics.iloc[0]
    best = xc[xc["lag_periode"] > 0].sort_values("korelasi", ascending=False).head(1)
    gr_sig = gr[gr.get("p_value", pd.Series(dtype=float)) < 0.05] if "p_value" in gr else pd.DataFrame()
    p = pl.iloc[0]
    lines = [
        "# Ringkasan Backtest Sistem Peringatan Dini MBG", "",
        f"- Resolusi waktu: {args.freq}; jendela prediksi: {args.window} jam; ambang z: {args.threshold}",
        f"- Periode dianalisis: {int(m['periode_total'])} (volume rendah < {args.min_n} cuitan: {int(m['periode_volume_rendah'])})",
        f"- Alarm: {int(m['jumlah_alarm'])}; kejadian resmi: {int(m['jumlah_kejadian'])}",
        f"- Precision: {fmt(m['precision'])}; recall: {fmt(m['recall'])}; F1: {fmt(m['f1'])}",
        f"- Median lead time: {fmt(m['median_lead_time_jam'],1)} jam (rata-rata {fmt(m['mean_lead_time_jam'],1)} jam)",
        f"- Uji permutasi: recall nyata {fmt(p['recall_nyata'])} vs acak {fmt(p['recall_acak_rata2'])} "
        f"(p = {fmt(p['p_value_permutasi'],3)}, {int(p['n_permutasi'])} permutasi)",
    ]
    if len(best):
        lines.append(f"- Korelasi silang tertinggi saat sinyal mendahului: lag {int(best['lag_periode'].iloc[0])} periode, r = {fmt(best['korelasi'].iloc[0])}")
    if "p_value" in gr:
        lines.append(f"- Uji Granger (sinyal → kejadian): lag signifikan (p<0,05): "
                     f"{', '.join(str(int(l)) for l in gr_sig['lag']) if len(gr_sig) else 'tidak ada'}")
    else:
        lines.append(f"- Uji Granger: {gr.iloc[0].get('catatan','—')}")
    lines += ["", "## Draf kalimat untuk naskah (sesuaikan dengan angka di atas)", "",
              f"Backtest retrospektif terhadap {int(m['jumlah_kejadian'])} kejadian resmi selama periode penelitian menunjukkan bahwa "
              f"{fmt(m['recall']*100 if pd.notna(m['recall']) else np.nan,0)}% kejadian didahului alarm dalam jendela {args.window} jam, "
              f"dengan median lead time {fmt(m['median_lead_time_jam'],1)} jam dan precision {fmt(m['precision'])}. "
              f"Recall ini {'lebih tinggi secara signifikan' if p['p_value_permutasi']<0.05 else 'tidak berbeda signifikan'} "
              f"dibandingkan tanggal kejadian acak (p = {fmt(p['p_value_permutasi'],3)}).", "",
              "Catatan: jika p permutasi ≥ 0,05, JANGAN klaim kemampuan prediktif; laporkan sebagai temuan negatif/eksploratif."]
    open(path, "w", encoding="utf-8").write("\n".join(lines))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tweets", required=True)
    ap.add_argument("--events", required=True)
    ap.add_argument("--edges", default=None)
    ap.add_argument("--out", default="hasil_early_warning")
    ap.add_argument("--freq", default="1D", help="resolusi: 1D, 12h, 6h")
    ap.add_argument("--roll", type=int, default=7, help="jumlah periode baseline rolling")
    ap.add_argument("--threshold", type=float, default=1.5, help="ambang z-score alarm")
    ap.add_argument("--window", type=float, default=72, help="jendela prediksi (jam)")
    ap.add_argument("--min-n", dest="min_n", type=int, default=5)
    ap.add_argument("--max-lag", type=int, default=5)
    ap.add_argument("--perm", type=int, default=1000)
    ap.add_argument("--tz", default="Asia/Jakarta")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    tw = load_tweets(args.tweets, args.tz)
    ev = load_events(args.events, args.tz)
    net = network_metrics(args.edges, args.freq, args.tz) if args.edges else None
    s = build_signals(tw, args.freq, args.roll, net, min_n=args.min_n)
    alerts, lead, metrics = evaluate(s, ev, args.threshold, args.window, args.freq)
    y = event_series(s, ev)
    xc = xcorr(s, y, args.max_lag)
    gr = granger(s, y, args.max_lag)
    pl = placebo(s, ev, args.threshold, args.window, args.freq, args.perm)

    s.to_csv(f"{args.out}/signals.csv")
    alerts.to_csv(f"{args.out}/alerts.csv")
    lead.to_csv(f"{args.out}/event_leadtime.csv", index=False)
    metrics.to_csv(f"{args.out}/metrics.csv", index=False)
    xc.to_csv(f"{args.out}/xcorr.csv", index=False)
    gr.to_csv(f"{args.out}/granger.csv", index=False)
    pl.to_csv(f"{args.out}/placebo.csv", index=False)
    plot(s, ev, args.threshold, f"{args.out}/plot_signals.png")
    summary(metrics, xc, gr, pl, args, f"{args.out}/RINGKASAN.md")
    print(open(f"{args.out}/RINGKASAN.md", encoding="utf-8").read())


if __name__ == "__main__":
    main()
