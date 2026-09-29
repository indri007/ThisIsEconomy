#!/usr/bin/env python3
"""Membuat data SINTETIS untuk mencoba ew_backtest.py. Jangan dipakai sebagai hasil penelitian."""
import numpy as np
import pandas as pd

rng = np.random.default_rng(7)
start = pd.Timestamp("2026-03-01", tz="Asia/Jakarta")
days = 92
events = [15, 34, 51, 70, 83]  # hari ke-, kejadian sintetis
emos = ["Disgust", "Anger", "Fear", "Joy", "Trust", "Neutral", "Sadness", "Interest", "Surprise"]
base_p = np.array([.35, .12, .05, .03, .05, .25, .08, .04, .03])

rows, edges = [], []
for d in range(days):
    near = any(0 <= e - d <= 2 for e in events)  # 0-2 hari SEBELUM kejadian: lonjakan
    n = rng.poisson(90 if near else 35)
    p = base_p.copy()
    if near:
        p[0] += .25; p[5] -= .15; p[4] -= .03
    p = np.clip(p, .005, None); p /= p.sum()
    for _ in range(n):
        t = start + pd.Timedelta(days=d, seconds=int(rng.integers(0, 86400)))
        e = rng.choice(emos, p=p)
        sar = int(rng.random() < (.45 if near else .2))
        rows.append({"tweet_id": len(rows), "created_at": t.isoformat(), "emotion": e, "sarcasm": sar})
        edges.append({"source": f"u{rng.integers(0, 900)}", "target": f"u{rng.integers(0, 60)}", "created_at": t.isoformat()})

pd.DataFrame(rows).to_csv("demo_tweets.csv", index=False)
pd.DataFrame(edges).to_csv("demo_edges.csv", index=False)
pd.DataFrame([{"event_time": (start + pd.Timedelta(days=e, hours=10)).isoformat(),
               "event_type": "contoh", "description": f"KEJADIAN SINTETIS hari ke-{e}",
               "source_url": "https://contoh.invalid"} for e in events]).to_csv("demo_events.csv", index=False)
print("demo_tweets.csv, demo_edges.csv, demo_events.csv dibuat")
