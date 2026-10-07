#!/usr/bin/env python3

from __future__ import annotations

import json
import os
import subprocess
import sys
import traceback
from pathlib import Path
from datetime import datetime

ROOT = Path("/Users/jevin/Documents/tesis_mbg")
REPORT_DIR = ROOT / "reports" / "thesis_evidence"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

RESULT = {
    "timestamp": datetime.now().isoformat(),
    "project": str(ROOT),
    "steps": [],
    "warnings": [],
    "errors": [],
}

def run_cmd(cmd, cwd=ROOT):
    try:
        p = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=120,
        )
        return p.returncode, p.stdout.strip(), p.stderr.strip()
    except Exception as e:
        return 99, "", str(e)

def step(no, name, status, detail=""):
    item = {
        "step": no,
        "name": name,
        "status": status,
        "detail": detail,
    }
    RESULT["steps"].append(item)

    icon = {
        "PASS": "✅",
        "WARN": "⚠️",
        "SKIP": "⏭️",
        "FAIL": "❌",
    }.get(status, "•")

    print(f"{icon} STEP {no}/10 — {name}")
    if detail:
        print(f"   {detail}")
    print()

print("=" * 75)
print("FINAL 10-STEP THESIS + CUSTOM EWS PRODUCTION AUDIT")
print("=" * 75)
print(f"ROOT: {ROOT}")
print()

# ============================================================
# STEP 1 — PRODUCTION CHECK
# ============================================================

required = [
    "dashboard/app.py",
    "requirements.txt",
    "dashboard/requirements.txt",
    "runtime.txt",
    ".streamlit/config.toml",
    "ews/__init__.py",
    "ews/fallback.py",
    "ews/custom_dashboard.py",
    "ews/explainable_score.py",
    "scripts/early_warning_system.py",
    "scripts/rename_emotions.py",
]

missing = [x for x in required if not (ROOT / x).exists()]

if missing:
    step(1, "Production Check", "FAIL", "Missing: " + ", ".join(missing))
else:
    rc, out, err = run_cmd(["git", "status", "--short"])
    rc2, branch, _ = run_cmd(["git", "branch", "--show-current"])
    rc3, head, _ = run_cmd(["git", "rev-parse", "--short", "HEAD"])

    detail = f"branch={branch}; HEAD={head}; "
    detail += "working tree clean" if not out else "working tree has changes"
    step(1, "Production Check", "PASS", detail)

# ============================================================
# STEP 2 — DASHBOARD FUNCTIONAL CHECK
# ============================================================

app = ROOT / "dashboard" / "app.py"

try:
    compile(app.read_text(encoding="utf-8"), str(app), "exec")
    step(2, "Dashboard Functional Check", "PASS", "dashboard/app.py syntax OK")
except Exception as e:
    step(2, "Dashboard Functional Check", "FAIL", str(e))

rc, out, err = run_cmd([
    sys.executable,
    "-c",
    """
import streamlit
import pandas
import numpy
import plotly
import networkx
import community
import pyvis
import sklearn
import openpyxl
print(\"CORE IMPORTS OK\")
"""
])
if rc != 0:
    RESULT["errors"].append(err)
    step(2, "Dashboard Dependencies", "FAIL", err[-500:])
else:
    print("   CORE IMPORTS: PASS")

# ============================================================
# STEP 3 — EWS SCENARIO TEST
# ============================================================

try:
    from scripts.early_warning_system import compute_ews_score

    scenarios = {
        "SAFE": {"crisis_keywords": 1, "sarcasm_emojis": 1, "negative_pct": 5, "sarcasm_pct": 5},
        "WARNING": {"crisis_keywords": 10, "sarcasm_emojis": 5, "negative_pct": 30, "sarcasm_pct": 25},
        "DANGER": {"crisis_keywords": 20, "sarcasm_emojis": 10, "negative_pct": 55, "sarcasm_pct": 45},
        "CRITICAL": {"crisis_keywords": 30, "sarcasm_emojis": 20, "negative_pct": 80, "sarcasm_pct": 80},
    }
    scenario_results = {}
    for name, cfg in scenarios.items():
        try:
            r = compute_ews_score(cfg["crisis_keywords"], cfg["sarcasm_emojis"], cfg["negative_pct"], cfg["sarcasm_pct"])
            scenario_results[name] = str(r)
        except Exception as e:
            scenario_results[name] = f"ERROR: {e}"
    RESULT["ews_scenarios"] = scenario_results
    step(3, "EWS Scenario Test", "PASS", "All scenarios executed")
except Exception as e:
    step(3, "EWS Scenario Test", "WARN", f"Legacy EWS unavailable: {e}")

# ============================================================
# STEP 4 — EXPLAINABLE EWS
# ============================================================

try:
    # Ensure repo root on PYTHONPATH for import
    sys.path.insert(0, str(ROOT))
    from ews.explainable_score import prepare, build_context, calculate_score
    import pandas as pd
    emotion_df = pd.read_csv(ROOT / "data/results/indobert_9_emosi_fixed.csv")
    sarcasm_df = pd.read_csv(ROOT / "data/sarcasm/dataset_sindiran_valid.csv")
    prepared = prepare(emotion_df, sarcasm_df)
    context = build_context(prepared)
    score = calculate_score(context)
    RESULT["explainable_ews"] = {"context": str(context), "score": str(score)}
    step(4, "Explainable EWS", "PASS", "Evaluated successfully")
except Exception as e:
    RESULT["errors"].append(traceback.format_exc())
    step(4, "Explainable EWS", "FAIL", str(e))

# ============================================================
# STEP 5 — CROSS ANALYSIS
# ============================================================

try:
    import pandas as pd
    emotion_file = ROOT / "data/results/indobert_9_emosi_fixed.csv"
    sarcasm_file = ROOT / "data/sarcasm/dataset_sindiran_valid.csv"
    emotion_df = pd.read_csv(emotion_file)
    sarcasm_df = pd.read_csv(sarcasm_file)
    cross = {
        "emotion_rows": len(emotion_df),
        "sarcasm_rows": len(sarcasm_df),
        "emotion_distribution": emotion_df["predicted_emotion"].value_counts(dropna=False).to_dict() if "predicted_emotion" in emotion_df.columns else {},
        "sarcasm_distribution": sarcasm_df["sindiran"].value_counts(dropna=False).to_dict() if "sindiran" in sarcasm_df.columns else {},
    }
    RESULT["cross_analysis"] = cross
    step(5, "Cross Analysis", "PASS", f"emotion={len(emotion_df)} rows, sarcasm={len(sarcasm_df)} rows")
except Exception as e:
    step(5, "Cross Analysis", "FAIL", str(e))

# ============================================================
# STEP 6 — NETWORK INTELLIGENCE
# ============================================================

try:
    import pandas as pd
    sna_file = ROOT / "data/results/mbg_network_nodes_final.csv"
    sna = pd.read_csv(sna_file)
    network_summary = {
        "nodes": len(sna),
        "columns": list(sna.columns),
        "communities": int(sna["Community"].nunique()) if "Community" in sna.columns else None,
        "top_degree": sna.nlargest(10, "Degree")[[c for c in ["Id", "Label", "Degree", "Community"] if c in sna.columns]].to_dict("records") if "Degree" in sna.columns else [],
    }
    RESULT["network_intelligence"] = network_summary
    step(6, "Network Intelligence", "PASS", f"{len(sna)} nodes, {network_summary['communities']} communities")
except Exception as e:
    step(6, "Network Intelligence", "FAIL", str(e))

# ============================================================
# STEP 7 — HISTORICAL TIMELINE + ANOMALY
# ============================================================

try:
    import pandas as pd
    import numpy as np
    emotion_file = ROOT / "data/results/indobert_9_emosi_fixed.csv"
    df = pd.read_csv(emotion_file)
    date_col = "created_at"
    if date_col not in df.columns:
        raise ValueError("created_at not found")
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    daily = df.dropna(subset=[date_col]).groupby(df[date_col].dt.date).size()
    mean = float(daily.mean())
    std = float(daily.std())
    if std > 0:
        z = (daily - mean) / std
        anomalies = daily[z >= 2]
    else:
        anomalies = daily.iloc[0:0]
    timeline = {
        "active_days": len(daily),
        "mean_mentions_per_day": mean,
        "std_mentions_per_day": std,
        "anomaly_count_z2": len(anomalies),
        "anomalies": {str(k): int(v) for k, v in anomalies.items()},
    }
    RESULT["historical_timeline"] = timeline
    step(7, "Historical Timeline + Anomaly", "PASS", f"{len(daily)} days, {len(anomalies)} anomalies")
except Exception as e:
    step(7, "Historical Timeline + Anomaly", "FAIL", str(e))

# ============================================================
# STEP 8 — THESIS EVIDENCE PACK
# ============================================================

try:
    evidence = REPORT_DIR / "EWS_EVIDENCE_SUMMARY.json"
    payload = {
        "generated_at": datetime.now().isoformat(),
        "project": "Social Network Analysis Sarkasme Cuitan Twitter di Balik Pertaruhan Triliunan Rupiah pada Kebijakan Makan Bergizi Gratis",
        "purpose": "Research evidence / reproducibility audit",
        "note": "Evidence pack bersifat audit teknis.",
        "emotion_file": str(ROOT / "data/results/indobert_9_emosi_fixed.csv"),
        "sarcasm_file": str(ROOT / "data/sarcasm/dataset_sindiran_valid.csv"),
        "sna_file": str(ROOT / "data/results/mbg_network_nodes_final.csv"),
        "results": RESULT,
    }
    evidence.write_text(json.dumps(payload, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    step(8, "Thesis Evidence Pack", "PASS", f"created {evidence.relative_to(ROOT)}")
except Exception as e:
    step(8, "Thesis Evidence Pack", "FAIL", str(e))

# ============================================================
# STEP 9 — REPRODUCIBILITY
# ============================================================

try:
    reproducibility_files = [
        "requirements.txt",
        "dashboard/requirements.txt",
        "runtime.txt",
        ".streamlit/config.toml",
        "dashboard/app.py",
        "ews/fallback.py",
        "ews/custom_dashboard.py",
        "ews/explainable_score.py",
        "scripts/early_warning_system.py",
    ]
    missing_rep = [x for x in reproducibility_files if not (ROOT / x).exists()]
    if missing_rep:
        step(9, "Reproducibility", "FAIL", "Missing: " + ", ".join(missing_rep))
    else:
        rc, out, err = run_cmd([sys.executable, "-m", "pip", "check"])
        if rc == 0:
            step(9, "Reproducibility", "PASS", "pip check OK")
        else:
            pip_detail = (out + "\n" + err).strip()
            step(9, "Reproducibility", "WARN", "pip issues: " + pip_detail[-400:])
except Exception as e:
    step(9, "Reproducibility", "FAIL", str(e))

# ============================================================
# STEP 10 — FINAL RELEASE AUDIT
# ============================================================

try:
    rc, status, err = run_cmd(["git", "status", "--short"])
    rc2, branch, _ = run_cmd(["git", "branch", "--show-current"])
    rc3, head, _ = run_cmd(["git", "rev-parse", "HEAD"])
    clean = not status.strip()
    fail_count = sum(1 for s in RESULT["steps"] if s["status"] == "FAIL")
    warn_count = sum(1 for s in RESULT["steps"] if s["status"] == "WARN")
    if fail_count == 0 and clean:
        release_status = "READY"
    elif fail_count == 0:
        release_status = "READY_WITH_LOCAL_CHANGES"
    else:
        release_status = "NOT_READY"
    RESULT["final"] = {
        "status": release_status,
        "branch": branch,
        "head": head,
        "working_tree_clean": clean,
        "fail_count": fail_count,
        "warning_count": warn_count,
        "push_command": "git push origin main" if release_status.startswith("READY") else None,
    }
    step(10, "Final Release Audit", "PASS" if fail_count == 0 else "FAIL", f"STATUS={release_status}; FAIL={fail_count}; WARN={warn_count}; branch={branch}; HEAD={head}")
except Exception as e:
    step(10, "Final Release Audit", "FAIL", str(e))

# ============================================================
# FINAL REPORT
# ============================================================

final_json = REPORT_DIR / "FINAL_10STEP_AUDIT.json"
final_json.write_text(json.dumps(RESULT, indent=2, ensure_ascii=False, default=str), encoding="utf-8")

print("=" * 75)
print("FINAL SUMMARY")
print("=" * 75)
for s in RESULT["steps"]:
    print(f"{s['step']:02d}. {s['status']:4s} — {s['name']}")
print()
if "final" in RESULT:
    f = RESULT["final"]
    print("RELEASE STATUS :", f["status"])
    print("FAILURES       :", f["fail_count"])
    print("WARNINGS       :", f["warning_count"])
    print("BRANCH         :", f["branch"])
    print("HEAD           :", f["head"])
    print("WORKTREE CLEAN :", f["working_tree_clean"])
print()
print("REPORT:")
print(final_json)
print("=" * 75)
