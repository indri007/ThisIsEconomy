from pathlib import Path
import sys
import importlib
import subprocess
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

REPORTS = ROOT / "reports"
REPORTS.mkdir(exist_ok=True)

results = {}

def check(name, fn):
    try:
        value = fn()
        results[name] = "PASS"
        print(f"✅ {name:<25} PASS")
        return value
    except Exception as e:
        results[name] = "FAIL"
        print(f"❌ {name:<25} FAIL — {e}")
        return None

print("\n" + "=" * 65)
print("CUSTOM EWS v2 — FINAL AUDIT")
print("=" * 65)

# 1. Python
check(
    "Python 3.12",
    lambda: (
        sys.version_info.major == 3
        and sys.version_info.minor == 12
    ) or (_ for _ in ()).throw(
        RuntimeError(f"Python {sys.version_info.major}.{sys.version_info.minor}")
    )
)

# 2. Required files
required_files = [
    "dashboard/app.py",
    "requirements.txt",
    "dashboard/requirements.txt",
    "runtime.txt",
    ".streamlit/config.toml",
    "ews/__init__.py",
    "ews/fallback.py",
    "ews/custom_dashboard.py",
]

for f in required_files:
    check(f"File: {f}", lambda f=f: (
        (ROOT / f).exists()
        or (_ for _ in ()).throw(FileNotFoundError(f))
    ))

# 3. Dataset
emotion_file = ROOT / "data/results/indobert_9_emosi_fixed.csv"
sarcasm_file = ROOT / "data/sarcasm/dataset_sindiran_valid.csv"
sna_file = ROOT / "data/results/mbg_network_nodes_final.csv"

emotion_df = check(
    "Emotion dataset",
    lambda: pd.read_csv(emotion_file)
)

sarcasm_df = check(
    "Sarcasm dataset",
    lambda: pd.read_csv(sarcasm_file)
)

sna_df = check(
    "SNA dataset",
    lambda: pd.read_csv(sna_file)
)

# 4. Emotion validation
if emotion_df is not None:
    def validate_emotion():
        required = {"id", "text", "predicted_emotion"}
        missing = required - set(emotion_df.columns)
        if missing:
            raise ValueError(f"missing columns: {missing}")

        emotion_df["predicted_emotion"] = (
            emotion_df["predicted_emotion"]
            .astype(str)
            .str.strip()
        )

        distribution = (
            emotion_df["predicted_emotion"]
            .value_counts()
            .rename_axis("emotion")
            .reset_index(name="count")
        )

        distribution["percentage"] = (
            distribution["count"]
            / len(emotion_df)
            * 100
        ).round(2)

        distribution.to_csv(
            REPORTS / "emotion_validation.csv",
            index=False
        )

        return distribution

    emotion_distribution = check(
        "Emotion validation",
        validate_emotion
    )

# 5. Sarcasm validation
if sarcasm_df is not None:
    def validate_sarcasm():
        required = {"id", "text", "sindiran"}
        missing = required - set(sarcasm_df.columns)

        if missing:
            raise ValueError(f"missing columns: {missing}")

        result = (
            sarcasm_df["sindiran"]
            .astype(str)
            .value_counts()
            .rename_axis("sarcasm")
            .reset_index(name="count")
        )

        result["percentage"] = (
            result["count"]
            / len(sarcasm_df)
            * 100
        ).round(2)

        result.to_csv(
            REPORTS / "sarcasm_validation.csv",
            index=False
        )

        return result

    sarcasm_distribution = check(
        "Sarcasm validation",
        validate_sarcasm
    )

# 6. SNA validation
if sna_df is not None:
    def validate_sna():
        required = {"Id", "Degree", "Betweenness", "Community"}
        missing = required - set(sna_df.columns)

        if missing:
            raise ValueError(f"missing columns: {missing}")

        summary = {
            "nodes": int(len(sna_df)),
            "communities": int(sna_df["Community"].nunique()),
            "degree_mean": float(sna_df["Degree"].mean()),
            "degree_max": float(sna_df["Degree"].max()),
            "betweenness_mean": float(sna_df["Betweenness"].mean()),
            "betweenness_max": float(sna_df["Betweenness"].max()),
        }

        with open(
            REPORTS / "sna_validation.json",
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(summary, f, indent=2)

        pd.DataFrame([summary]).to_csv(
            REPORTS / "sna_validation.csv",
            index=False
        )

        return summary

    sna_summary = check(
        "SNA validation",
        validate_sna
    )

# 7. Anomaly detection
if emotion_df is not None:
    def validate_anomaly():
        if "created_at" not in emotion_df.columns:
            raise ValueError("created_at tidak tersedia")

        df = emotion_df.copy()

        df["created_at"] = pd.to_datetime(
            df["created_at"],
            errors="coerce"
        )

        df = df.dropna(subset=["created_at"])

        daily = (
            df.groupby(df["created_at"].dt.date)
            .size()
            .reset_index(name="mentions")
        )

        daily["date"] = pd.to_datetime(daily["created_at"])
        daily = daily.drop(columns=["created_at"])

        daily["rolling_mean"] = (
            daily["mentions"]
            .rolling(7, min_periods=3)
            .mean()
        )

        daily["rolling_std"] = (
            daily["mentions"]
            .rolling(7, min_periods=3)
            .std()
        )

        global_mean = daily["mentions"].mean()
        global_std = daily["mentions"].std()

        if global_std and global_std > 0:
            daily["z_score"] = (
                daily["mentions"] - global_mean
            ) / global_std
        else:
            daily["z_score"] = 0.0

        daily["is_anomaly"] = daily["z_score"] >= 2

        daily.to_csv(
            REPORTS / "anomaly_events.csv",
            index=False
        )

        return daily[daily["is_anomaly"]]

    anomaly_events = check(
        "Anomaly detection",
        validate_anomaly
    )

# 8. EWS components
ews_modules = [
    "ews.fallback",
    "ews.custom_dashboard",
]

for module in ews_modules:
    check(
        f"Import {module}",
        lambda module=module: importlib.import_module(module)
    )

# 9. Dashboard syntax
def compile_dashboard():
    app = ROOT / "dashboard/app.py"
    subprocess.run(
        [sys.executable, "-m", "py_compile", str(app)],
        check=True,
        capture_output=True,
        text=True,
    )

check(
    "Dashboard syntax",
    compile_dashboard
)

# 10. Git diff check
def git_diff_check():
    subprocess.run(
        ["git", "diff", "--check"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

check(
    "Git diff check",
    git_diff_check
)

# Final report
print("\n" + "=" * 65)
print("SUMMARY")
print("=" * 65)

passed = sum(v == "PASS" for v in results.values())
total = len(results)

for name, status in results.items():
    print(f"{'✅' if status == 'PASS' else '❌'} {name}: {status}")

print("\n" + "-" * 65)
print(f"TOTAL : {passed}/{total}")
print(f"STATUS: {'READY' if passed == total else 'NOT READY'}")
print("-" * 65)

# Evidence summary
summary = {
    "total_checks": total,
    "passed": passed,
    "failed": total - passed,
    "status": "READY" if passed == total else "NOT READY",
    "emotion_rows": (
        len(emotion_df) if emotion_df is not None else None
    ),
    "sarcasm_rows": (
        len(sarcasm_df) if sarcasm_df is not None else None
    ),
    "sna_nodes": (
        len(sna_df) if sna_df is not None else None
    ),
    "anomaly_events": (
        len(anomaly_events) if anomaly_events is not None else None
    ),
}

with open(
    REPORTS / "EWS_FINAL_AUDIT.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(summary, f, indent=2, default=str)

print(f"\nReport: {REPORTS / 'EWS_FINAL_AUDIT.json'}")
print(f"Reports: {REPORTS}")
