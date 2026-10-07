import os
from pathlib import Path
import pandas as pd
import streamlit as st
from dashboard.modules.config import get_data_path, PROJECT_ROOT


@st.cache_data(ttl=3600)
def load_emotion_data():
    return pd.read_csv(get_data_path("indobert_9_emosi_fixed.csv"))


@st.cache_data(ttl=3600)
def load_network_data():
    edge_path = get_data_path("network_edges.csv")
    node_path = get_data_path("sna_degree.csv")
    edges = pd.read_csv(edge_path)
    nodes = pd.read_csv(node_path) if os.path.exists(node_path) else None
    return edges, nodes


def load_final_evaluation():
    base_dir = Path(__file__).resolve().parent.parent
    candidates = [
        base_dir.parent / "results",
        base_dir / "results",
        base_dir.parent.parent / "results",
        Path.cwd() / "results",
        Path.cwd() / "mbg-sna-github" / "results"
    ]
    res_dir = None
    for c in candidates:
        if (c / "FINAL_MODEL_COMPARISON.csv").exists():
            res_dir = c
            break
    if res_dir is None:
        raise FileNotFoundError("Results directory with final evaluation CSVs not found.")
    v2 = res_dir / "indobert_group_aware_v2"
    if (v2 / "metrics_v2.csv").exists() and (v2 / "classification_report_v2.csv").exists():
        m = pd.read_csv(v2 / "metrics_v2.csv").iloc[0]
        rows = []
        for fname, name in [("tfidf_logreg_metrics.csv", "TF-IDF + Logistic Regression"), ("tfidf_svm_metrics.csv", "TF-IDF + Linear SVM")]:
            if (v2 / fname).exists():
                b = pd.read_csv(v2 / fname).iloc[0]
                rows.append({"Model": name, "Protocol": "Group-aware train/val/test (v2)", "Train_N": int(b["Train_N"]), "Test_N": int(b["Test_N"]),
                             "Accuracy": b["Accuracy"], "Macro_F1": b["Macro_F1"], "Weighted_F1": b["Weighted_F1"]})
        rows.append({"Model": "IndoBERT Group-Aware", "Protocol": "Group-aware train/val/test (v2)", "Train_N": 3785, "Test_N": int(m["Test_N"]),
                     "Accuracy": m["Accuracy"], "Macro_F1": m["Macro_F1"], "Weighted_F1": m["Weighted_F1"]})
        cr = pd.read_csv(v2 / "classification_report_v2.csv")
        cr = cr[~cr["Emotion"].isin(["accuracy", "macro avg", "weighted avg"])].copy()
        tot = cr["support"].sum()
        per_class = pd.DataFrame({"label": cr["Emotion"], "support": cr["support"].astype(int), "precision": cr["precision"],
                                  "recall": cr["recall"], "f1": cr["f1-score"], "test_percentage": cr["support"] / tot * 100})
        per_class = per_class.sort_values("support", ascending=False)
        return {
            "comparison": pd.DataFrame(rows),
            "per_class": per_class,
            "distribution": pd.read_csv(res_dir / "FINAL_CLASS_DISTRIBUTION.csv"),
            "indobert_metrics": pd.read_csv(v2 / "metrics_v2.csv"),
            "results_dir": res_dir,
            "cm_dir": v2,
            "protocol": "v2",
        }
    return {
        "comparison": pd.read_csv(res_dir / "FINAL_MODEL_COMPARISON.csv"),
        "per_class": pd.read_csv(res_dir / "FINAL_PER_CLASS_ANALYSIS.csv"),
        "distribution": pd.read_csv(res_dir / "FINAL_CLASS_DISTRIBUTION.csv"),
        "indobert_metrics": pd.read_csv(res_dir / "FINAL_indobert_metrics.csv"),
        "results_dir": res_dir,
        "cm_dir": res_dir,
        "protocol": "v1",
    }
