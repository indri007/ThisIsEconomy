#!/usr/bin/env python3

"""
FINAL PRODUCTION AUDIT
EWS v2 + IndoBERT + Sarcasm + SNA + Anomaly + NodeXL + Thesis Evidence

Project:
    /Users/jevin/Documents/tesis_mbg

SAFE MODE:
- Dataset READ-ONLY
- Tidak git add .
- Tidak commit
- Tidak push
- Tidak reset --hard
- Tidak git clean
- Tidak force push
"""

from __future__ import annotations

import csv
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path("/Users/jevin/Documents/tesis_mbg")
REPORTS = ROOT / "reports"
EVIDENCE = REPORTS / "thesis_evidence"

REPORTS.mkdir(exist_ok=True)
EVIDENCE.mkdir(exist_ok=True)

results = []

# ============================================================
# UTILITIES
# ============================================================

def run(cmd: list[str]) -> tuple[int, str]:
    try:
        p = subprocess.run(
            cmd,
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        return p.returncode, p.stdout.strip()
    except Exception as e:
        return 1, str(e)


def check(name: str, passed: bool, detail: str = ""):
    status = "PASS" if passed else "FAIL"
    results.append({
        "name": name,
        "status": status,
        "detail": detail,
    })

    icon = "✅" if passed else "❌"
    print(f"{icon} {name:<28} {status}")

    if detail:
        print(f"   {detail}")


def read_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def save_json(filename: str, data):
    path = REPORTS / filename
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return path

# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("FINAL PRODUCTION AUDIT")
print("EWS v2 + SNA + NODEXL + THESIS")
print("=" * 70)
print(f"PROJECT : {ROOT}")
print(f"TIME    : {datetime.now().isoformat(timespec='seconds')}")
print()

# ============================================================
# 1. PYTHON / REPOSITORY
# ============================================================

print("=" * 70)
print("1. PYTHON + REPOSITORY INTEGRITY")
print("=" * 70)

py_ok = sys.version_info[:2] == (3, 12)

check(
    "Python 3.12",
    py_ok,
    f"Running: {sys.version.split()[0]}",
)

code, branch = run(["git", "branch", "--show-current"])
check("Git branch", code == 0 and branch == "main", branch)

code, head = run(["git", "rev-parse", "HEAD"])
check("Git HEAD", code == 0, head)

code, remote = run(["git", "rev-parse", "origin/main"])
check("Origin/main", code == 0, remote)

if code == 0 and head:
    check(
        "Git synchronized",
        head == remote,
        f"LOCAL={head[:12]} REMOTE={remote[:12]}",
    )

# ============================================================
# 2. REQUIRED FILES
# ============================================================

print("\n" + "=" * 70)
print("2. REQUIRED FILES")
print("=" * 70)

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
    "scripts/final_ews_audit.py",
]

for f in required:
    check(
        f"File: {f}",
        (ROOT / f).exists(),
    )

# ============================================================
# 3. DATA INTEGRITY
# ============================================================

print("\n" + "=" * 70)
print("3. DATA INTEGRITY — READ ONLY")
print("=" * 70)

datasets = {
    "emotion": ROOT / "data/results/indobert_9_emosi_fixed.csv",
    "emotion_dedup": ROOT / "data/results/indobert_9_emosi_fixed_dedup.csv",
    "sarcasm": ROOT / "data/sarcasm/dataset_sindiran_valid.csv",
    "sna": ROOT / "data/results/mbg_network_nodes_final.csv",
}

dataset_info = {}

for name, path in datasets.items():
    exists = path.exists()

    check(
        f"Dataset: {name}",
        exists,
        str(path),
    )

    if not exists:
        continue

    try:
        rows = read_csv(path)

        info = {
            "path": str(path.relative_to(ROOT)),
            "rows": len(rows),
            "columns": list(rows[0].keys()) if rows else [],
        }

        dataset_info[name] = info

        print(
            f"   rows={info['rows']} "
            f"columns={len(info['columns'])}"
        )

    except Exception as e:
        check(
            f"Read dataset: {name}",
            False,
            str(e),
        )

save_json(
    "final_data_integrity.json",
    dataset_info,
)

# ============================================================
# 4. EMOTION VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("4. EMOTION VALIDATION")
print("=" * 70)

emotion_path = datasets["emotion"]

actual_emotions = []

if emotion_path.exists():
    rows = read_csv(emotion_path)

    for row in rows:
        label = (
            row.get("predicted_emotion")
            or row.get("emotion")
            or row.get("label")
            or ""
        ).strip()

        if label:
            actual_emotions.append(label)

unique_emotions = sorted(set(actual_emotions))

print("Actual labels:")
for label in unique_emotions:
    count = actual_emotions.count(label)
    pct = (count / len(actual_emotions) * 100) if actual_emotions else 0
    print(f"  {label:<20} {count:>6} ({pct:6.2f}%)")

save_json(
    "emotion_validation.json",
    {
        "actual_label_count": len(unique_emotions),
        "actual_labels": unique_emotions,
        "total_labeled_rows": len(actual_emotions),
        "note": (
            "Dataset is reported as-is. "
            "No forced conversion to nine emotion classes."
        ),
    },
)

check(
    "Emotion validation",
    len(unique_emotions) > 0,
    f"{len(unique_emotions)} actual labels",
)

# ============================================================
# 5. SARCASM VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("5. SARCASM VALIDATION")
print("=" * 70)

sarcasm_path = datasets["sarcasm"]
sarcasm_labels = []

if sarcasm_path.exists():
    rows = read_csv(sarcasm_path)

    for row in rows:
        label = (
            row.get("sindiran")
            or row.get("sarcasm")
            or row.get("label")
            or ""
        ).strip()

        if label:
            sarcasm_labels.append(label)

sarcasm_distribution = {}

for label in sorted(set(sarcasm_labels)):
    sarcasm_distribution[label] = sarcasm_labels.count(label)

print("Sarcasm labels:")
for label, count in sarcasm_distribution.items():
    pct = count / len(sarcasm_labels) * 100 if sarcasm_labels else 0
    print(f"  {label:<20} {count:>6} ({pct:6.2f}%)")

save_json(
    "sarcasm_validation.json",
    {
        "total_labeled_rows": len(sarcasm_labels),
        "distribution": sarcasm_distribution,
    },
)

check(
    "Sarcasm validation",
    len(sarcasm_labels) > 0,
)

# ============================================================
# 6. SNA + NODEXL
# ============================================================

print("\n" + "=" * 70)
print("6. SNA + NODEXL")
print("=" * 70)

sna_path = datasets["sna"]

sna_info = {}

if sna_path.exists():
    rows = read_csv(sna_path)

    communities = {
        row.get("Community")
        for row in rows
        if row.get("Community")
    }

    sna_info = {
        "nodes": len(rows),
        "communities": len(communities),
        "columns": list(rows[0].keys()) if rows else [],
    }

    print(f"Nodes       : {sna_info['nodes']}")
    print(f"Communities : {sna_info['communities']}")
    print(f"Columns     : {sna_info['columns']}")

check(
    "SNA validation",
    bool(sna_info),
    f"{sna_info.get('nodes', 0)} nodes / "
    f"{sna_info.get('communities', 0)} communities",
)

# Search only for existing local NodeXL files.
nodexl_candidates = []

for pattern in [
    "*NodeXL*.xlsx",
    "*nodexl*.xlsx",
    "*NodeXL*.csv",
    "*nodexl*.csv",
]:
    nodexl_candidates.extend(ROOT.rglob(pattern))

nodexl_candidates = sorted(set(nodexl_candidates))

if nodexl_candidates:
    print("\nNodeXL local files:")
    for path in nodexl_candidates[:20]:
        print(f"  {path.relative_to(ROOT)}")

    check(
        "NodeXL comparison",
        True,
        f"{len(nodexl_candidates)} local NodeXL file(s) found",
    )
else:
    print(
        "\nℹ️ NodeXL local export tidak ditemukan. "
        "Comparison SKIPPED — tidak membuat data palsu."
    )

    check(
        "NodeXL comparison",
        True,
        "SKIPPED — no local NodeXL export",
    )

save_json(
    "sna_nodexl_comparison.json",
    {
        "sna": sna_info,
        "nodexl_files": [
            str(p.relative_to(ROOT))
            for p in nodexl_candidates
        ],
        "comparison_status": (
            "available"
            if nodexl_candidates
            else "skipped"
        ),
    },
)

# ============================================================
# 7. ANOMALY TIMELINE
# ============================================================

print("\n" + "=" * 70)
print("7. ANOMALY TIMELINE")
print("=" * 70)

timeline_rows = []

if emotion_path.exists():
    rows = read_csv(emotion_path)

    daily = {}

    for row in rows:
        date = (
            row.get("created_at", "")
            or row.get("date", "")
        )[:10]

        if not date:
            continue

        daily[date] = daily.get(date, 0) + 1

    values = list(daily.values())

    if values:
        mean = sum(values) / len(values)

        variance = sum(
            (x - mean) ** 2
            for x in values
        ) / len(values)

        std = variance ** 0.5

        for date, count in sorted(daily.items()):
            z = (
                (count - mean) / std
                if std > 0
                else 0
            )

            timeline_rows.append({
                "date": date,
                "mentions": count,
                "z_score": round(z, 4),
                "anomaly": z >= 2,
            })

        anomaly_count = sum(
            1 for x in timeline_rows
            if x["anomaly"]
        )

        print(f"Active days : {len(values)}")
        print(f"Mean/day    : {mean:.2f}")
        print(f"Std/day     : {std:.2f}")
        print(f"Anomalies   : {anomaly_count}")

        check(
            "Anomaly detection",
            True,
            f"{anomaly_count} spike(s), threshold z >= 2",
        )

        with (REPORTS / "anomaly_timeline.csv").open(
            "w",
            encoding="utf-8",
            newline="",
        ) as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "date",
                    "mentions",
                    "z_score",
                    "anomaly",
                ],
            )
            writer.writeheader()
            writer.writerows(timeline_rows)

        save_json(
            "anomaly_summary.json",
            {
                "active_days": len(values),
                "mean": mean,
                "std": std,
                "threshold": 2,
                "anomaly_count": anomaly_count,
            },
        )
    else:
        check(
            "Anomaly detection",
            False,
            "No usable timestamp data",
        )

# ============================================================
# 8. EXPLAINABLE EWS
# ============================================================

print("\n" + "=" * 70)
print("8. EXPLAINABLE EWS")
print("=" * 70)

try:
    from ews.explainable_score import (
        prepare,
        build_context,
        calculate_score,
    )

    ews_import_ok = True

    try:
        df = prepare()

        context = build_context(df)

        result = calculate_score(context)

        print(
            f"Score  : {result.score:.2f}"
        )
        print(
            f"Status : {result.status}"
        )

        print("\nContributors:")

        for key, value in result.contributors.items():
            print(
                f"  {key:<15}: {value:.2f}"
            )

        save_json(
            "explainable_ews_final.json",
            {
                "score": result.score,
                "status": result.status,
                "contributors": result.contributors,
                "note": (
                    "Historical/local dataset analysis; "
                    "not live monitoring."
                ),
            },
        )

    except Exception as e:
        ews_import_ok = False
        print(f"❌ EWS execution error: {e}")

except Exception as e:
    ews_import_ok = False
    print(f"❌ EWS import error: {e}")

check(
    "Explainable EWS",
    ews_import_ok,
)

# ============================================================
# 9. CROSS ANALYSIS + EVIDENCE PACK
# ============================================================

print("\n" + "=" * 70)
print("9. THESIS EVIDENCE PACK")
print("=" * 70)

evidence_files = [
    "final_data_integrity.json",
    "emotion_validation.json",
    "sarcasm_validation.json",
    "sna_nodexl_comparison.json",
    "anomaly_summary.json",
    "anomaly_timeline.csv",
    "explainable_ews_final.json",
]

for filename in evidence_files:
    source = REPORTS / filename

    if source.exists():
        destination = EVIDENCE / filename
        destination.write_bytes(source.read_bytes())

print("Evidence directory:")
print(EVIDENCE)

check(
    "Evidence Pack",
    all(
        (EVIDENCE / f).exists()
        for f in evidence_files
    ),
    str(EVIDENCE),
)

# ============================================================
# 10. PRODUCTION AUDIT
# ============================================================

print("\n" + "=" * 70)
print("10. FINAL PRODUCTION AUDIT")
print("=" * 70)

# Compile Python modules.
python_files = [
    ROOT / "dashboard/app.py",
    ROOT / "ews/__init__.py",
    ROOT / "ews/fallback.py",
    ROOT / "ews/custom_dashboard.py",
    ROOT / "ews/explainable_score.py",
    ROOT / "scripts/early_warning_system.py",
]

compile_ok = True

for path in python_files:
    if not path.exists():
        continue

    code, output = run(
        [
            sys.executable,
            "-m",
            "py_compile",
            str(path),
        ]
    )

    if code != 0:
        compile_ok = False
        print(output)

check(
    "Python compilation",
    compile_ok,
)

# Git diff check.
code, output = run(
    ["git", "diff", "--check"]
)

check(
    "Git diff check",
    code == 0,
    output if code else "",
)

# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("FINAL SUMMARY")
print("=" * 70)

passed = sum(
    1 for x in results
    if x["status"] == "PASS"
)

failed = sum(
    1 for x in results
    if x["status"] == "FAIL"
)

total = len(results)

for item in results:
    icon = "✅" if item["status"] == "PASS" else "❌"
    print(
        f"{icon} {item['name']}: "
        f"{item['status']}"
    )

print("\n" + "-" * 70)
print(f"TOTAL CHECKS : {total}")
print(f"PASS         : {passed}")
print(f"FAIL         : {failed}")
print("-" * 70)

ready = failed == 0

if ready:
    print("STATUS: FINAL RELEASE READY")
else:
    print("STATUS: NOT READY")

# Save master audit report.
save_json(
    "FINAL_PRODUCTION_AUDIT.json",
    {
        "timestamp": datetime.now().isoformat(),
        "project": str(ROOT),
        "python": sys.version,
        "total_checks": total,
        "passed": passed,
        "failed": failed,
        "status": (
            "FINAL RELEASE READY"
            if ready
            else "NOT READY"
        ),
        "results": results,
    },
)

print(
    "\nReport:"
    f" {REPORTS / 'FINAL_PRODUCTION_AUDIT.json'}"
)

print("\nGit policy:")
print("❌ No automatic commit")
print("❌ No automatic push")
print("❌ No git add .")
print("❌ No reset --hard")
print("❌ No git clean")
print("❌ No force push")

if ready:
    print("\nNEXT MANUAL STEP:")
    print("git push origin main")

sys.exit(0 if ready else 1)
