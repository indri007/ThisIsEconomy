"""
ews/anomaly_detector.py
=======================
Modul Deteksi Anomali & Analisis Lonjakan Volume Harian untuk Custom EWS v2.
Menerapkan pemodelan statistik transparan (Rolling Average, Rolling Std, Z-Score)
pada runtut waktu cuitan historis MBG.

BATASAN METODOLOGIS:
- Seluruh analisis berbasis dataset historis (83 hari aktif periode Maret - Juni 2026).
- Anomali statistik mencerminkan lonjakan perhatian publik yang tidak biasa (spike event),
  bukan ramalan masa depan atau feeds real-time.
"""

from __future__ import annotations
from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np
from ews.config import EWS_WEIGHTS


def aggregate_daily_mentions(df: pd.DataFrame, date_col: str = "created_at") -> pd.DataFrame:
    """
    Mengelompokkan cuitan per tanggal kalender.
    Menghasilkan DataFrame dengan kolom ['date', 'mentions'].
    """
    if date_col not in df.columns:
        raise ValueError(f"Kolom tanggal '{date_col}' tidak ditemukan.")

    temp = df[[date_col]].copy()
    temp["datetime"] = pd.to_datetime(temp[date_col], errors="coerce")
    temp = temp.dropna(subset=["datetime"])

    if temp.empty:
        return pd.DataFrame(columns=["date", "mentions"])

    temp["date"] = temp["datetime"].dt.date
    daily = temp.groupby("date").size().reset_index(name="mentions")
    daily = daily.sort_values("date").reset_index(drop=True)
    return daily


def calculate_rolling_statistics(daily_df: pd.DataFrame, window: int = 7) -> pd.DataFrame:
    """
    Menghitung statistik bergerak (rolling mean & rolling standard deviation).
    """
    res = daily_df.copy()
    res["rolling_mean"] = res["mentions"].rolling(window=window, min_periods=1).mean().round(2)
    res["rolling_std"] = res["mentions"].rolling(window=window, min_periods=1).std().fillna(0).round(2)
    return res


def calculate_z_score(daily_df: pd.DataFrame) -> pd.DataFrame:
    """
    Menghitung Z-Score volume harian terhadap rata-rata dan deviasi standar global populasi.
    Formula: Z = (mentions - mean) / std
    """
    res = daily_df.copy()
    mean = res["mentions"].mean()
    std = res["mentions"].std()

    if std and not np.isnan(std) and std > 0:
        res["z_score"] = ((res["mentions"] - mean) / std).round(4)
    else:
        res["z_score"] = 0.0
    return res


def detect_spikes(daily_df: pd.DataFrame, threshold: float = 2.0, window: int = 7) -> pd.DataFrame:
    """
    Mendeteksi lonjakan anomali volume statistik.
    Menghasilkan kolom lengkap: ['date', 'mentions', 'rolling_mean', 'rolling_std', 'z_score', 'is_anomaly'].
    """
    if daily_df.empty:
        return pd.DataFrame(columns=["date", "mentions", "rolling_mean", "rolling_std", "z_score", "is_anomaly"])

    res = calculate_rolling_statistics(daily_df, window=window)
    res = calculate_z_score(res)
    res["is_anomaly"] = res["z_score"] >= threshold
    return res


def get_anomaly_metrics(df: pd.DataFrame, threshold: float = 2.0) -> Dict[str, Any]:
    """
    Menghitung metrik ringkasan anomali dan kontribusi risiko ke EWS v2.
    
    FORMULA BOBOT EWS:
    1. Anomaly Risk (0 - 15 Poin):
       - Berdasarkan frekuensi lonjakan z-score ekstrim (z >= threshold).
    2. Volume Risk (0 - 15 Poin):
       - Berdasarkan intensitas volume puncak relatif terhadap rata-rata harian normal.
    """
    daily = aggregate_daily_mentions(df)
    if daily.empty:
        return {
            "active_days": 0,
            "mean_mentions": 0.0,
            "std_mentions": 0.0,
            "spikes_count": 0,
            "spikes_df": pd.DataFrame(),
            "daily_df": pd.DataFrame(),
            "volume_risk_score": 0.0,
            "anomaly_risk_score": 0.0,
            "explanation": "Tidak ada data tanggal yang valid."
        }

    full_daily = detect_spikes(daily, threshold=threshold)
    mean_val = float(full_daily["mentions"].mean())
    std_val = float(full_daily["mentions"].std()) if not np.isnan(full_daily["mentions"].std()) else 0.0

    spikes_df = full_daily[full_daily["is_anomaly"]].sort_values("mentions", ascending=False)
    spikes_count = len(spikes_df)

    # 1. Skor Anomaly Risk (Maks 15 poin)
    # 1 spike = 4 poin, >= 4 spikes = 15 poin maksimum
    max_anomaly_risk = EWS_WEIGHTS["anomaly_risk"]
    anomaly_score = min(round((spikes_count / 4.0) * max_anomaly_risk, 1), max_anomaly_risk)

    # 2. Skor Volume Risk (Maks 15 poin)
    # Jika max volume harian > 5x mean -> risiko tinggi
    max_volume_risk = EWS_WEIGHTS["volume_risk"]
    max_day_volume = float(full_daily["mentions"].max()) if not full_daily.empty else 0.0
    vol_ratio = (max_day_volume / mean_val) if mean_val > 0 else 1.0
    # Rasio 15x mean atau lebih -> 15 poin (pada data MBG rasio 1022 / 63.41 = 16.1x)
    volume_score = min(round((vol_ratio / 15.0) * max_volume_risk, 1), max_volume_risk)

    top_spikes = spikes_df.head(5).to_dict(orient="records")

    explanation = (
        f"Terdeteksi {spikes_count} hari anomali volume statistik (Z-Score ≥ {threshold}) "
        f"dari {len(full_daily)} hari aktif (Mean: {mean_val:.1f}, Std: {std_val:.1f} cuitan/hari). "
        f"Puncak volume tertinggi: {int(max_day_volume):,} cuitan ({vol_ratio:.1f}x di atas rata-rata normal). "
        f"Kontribusi risiko: Anomali {anomaly_score}/{max_anomaly_risk} poin, Volume {volume_score}/{max_volume_risk} poin."
    )

    return {
        "active_days": len(full_daily),
        "mean_mentions": round(mean_val, 2),
        "std_mentions": round(std_val, 2),
        "spikes_count": spikes_count,
        "max_day_volume": int(max_day_volume),
        "max_volume_ratio": round(vol_ratio, 2),
        "spikes_df": spikes_df,
        "daily_df": full_daily,
        "top_spikes": top_spikes,
        "volume_risk_score": volume_score,
        "volume_risk_max": max_volume_risk,
        "anomaly_risk_score": anomaly_score,
        "anomaly_risk_max": max_anomaly_risk,
        "explanation": explanation
    }
