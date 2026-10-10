import os
from pathlib import Path
import pandas as pd
import streamlit as st
from dashboard.modules.config import get_data_path, PROJECT_ROOT


@st.cache_data(ttl=3600)
def load_emotion_data():
    """Defensively load emotion dataset with multi-path resolution and safe fallback."""
    candidates = [
        get_data_path("indobert_9_emosi_fixed.csv"),
        os.path.join(PROJECT_ROOT, "data", "results", "indobert_9_emosi_fixed.csv"),
        os.path.join(PROJECT_ROOT, "data", "indobert_9_emosi_fixed.csv"),
        os.path.join(PROJECT_ROOT, "results", "indobert_9_emosi_fixed.csv"),
        os.path.join(os.getcwd(), "data", "indobert_9_emosi_fixed.csv"),
        os.path.join(os.getcwd(), "data", "results", "indobert_9_emosi_fixed.csv"),
    ]
    for c in candidates:
        if c and os.path.exists(c):
            try:
                return pd.read_csv(c)
            except Exception as e:
                st.warning(f"Gagal membaca dataset emosi dari {c}: {e}")
    st.warning("Dataset indobert_9_emosi_fixed.csv tidak ditemukan di lokasi standar.")
    return pd.DataFrame(columns=["full_text", "label", "confidence", "sindiran"])


@st.cache_data(ttl=3600)
def load_network_data():
    """Defensively load network edges and nodes with multi-path resolution."""
    edge_candidates = [
        get_data_path("network_edges.csv"),
        os.path.join(PROJECT_ROOT, "data", "sna", "network_edges.csv"),
        os.path.join(PROJECT_ROOT, "data", "network_edges.csv"),
        os.path.join(PROJECT_ROOT, "results", "mbg_network_edges_final.csv"),
        os.path.join(os.getcwd(), "data", "network_edges.csv"),
    ]
    edge_path = None
    for c in edge_candidates:
        if c and os.path.exists(c):
            edge_path = c
            break

    node_candidates = [
        get_data_path("sna_degree.csv"),
        os.path.join(PROJECT_ROOT, "data", "results", "sna_degree.csv"),
        os.path.join(PROJECT_ROOT, "results", "mbg_network_nodes_final.csv"),
        os.path.join(PROJECT_ROOT, "data", "sna", "sna_degree.csv"),
        os.path.join(os.getcwd(), "data", "results", "sna_degree.csv"),
    ]
    node_path = None
    for c in node_candidates:
        if c and os.path.exists(c):
            node_path = c
            break

    if edge_path:
        try:
            edges = pd.read_csv(edge_path)
        except Exception:
            edges = pd.DataFrame(columns=["Source", "Target", "Weight"])
    else:
        st.warning("Dataset jaringan network_edges.csv tidak ditemukan.")
        edges = pd.DataFrame(columns=["Source", "Target", "Weight"])

    nodes = None
    if node_path:
        try:
            nodes = pd.read_csv(node_path)
        except Exception:
            nodes = None

    return edges, nodes


def load_final_evaluation():
    """Defensively load final evaluation metrics and comparisons."""
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
        st.warning("Direktori evaluasi akhir (results) tidak ditemukan.")
        empty_df = pd.DataFrame()
        return {
            "comparison": empty_df,
            "per_class": empty_df,
            "distribution": empty_df,
            "indobert_metrics": empty_df,
            "results_dir": base_dir.parent / "results",
            "cm_dir": base_dir.parent / "results",
            "protocol": "fallback",
        }

    v2 = res_dir / "indobert_group_aware_v2"
    if (v2 / "metrics_v2.csv").exists() and (v2 / "classification_report_v2.csv").exists():
        try:
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
            dist_df = pd.read_csv(res_dir / "FINAL_CLASS_DISTRIBUTION.csv") if (res_dir / "FINAL_CLASS_DISTRIBUTION.csv").exists() else pd.DataFrame()
            return {
                "comparison": pd.DataFrame(rows),
                "per_class": per_class,
                "distribution": dist_df,
                "indobert_metrics": pd.read_csv(v2 / "metrics_v2.csv"),
                "results_dir": res_dir,
                "cm_dir": v2,
                "protocol": "v2",
            }
        except Exception as e:
            st.warning(f"Peringatan saat memproses metrik evaluasi v2: {e}")

    try:
        return {
            "comparison": pd.read_csv(res_dir / "FINAL_MODEL_COMPARISON.csv") if (res_dir / "FINAL_MODEL_COMPARISON.csv").exists() else pd.DataFrame(),
            "per_class": pd.read_csv(res_dir / "FINAL_PER_CLASS_ANALYSIS.csv") if (res_dir / "FINAL_PER_CLASS_ANALYSIS.csv").exists() else pd.DataFrame(),
            "distribution": pd.read_csv(res_dir / "FINAL_CLASS_DISTRIBUTION.csv") if (res_dir / "FINAL_CLASS_DISTRIBUTION.csv").exists() else pd.DataFrame(),
            "indobert_metrics": pd.read_csv(res_dir / "FINAL_indobert_metrics.csv") if (res_dir / "FINAL_indobert_metrics.csv").exists() else pd.DataFrame(),
            "results_dir": res_dir,
            "cm_dir": res_dir,
            "protocol": "v1",
        }
    except Exception as e:
        st.warning(f"Peringatan saat memproses metrik evaluasi v1: {e}")
        return {
            "comparison": pd.DataFrame(),
            "per_class": pd.DataFrame(),
            "distribution": pd.DataFrame(),
            "indobert_metrics": pd.DataFrame(),
            "results_dir": res_dir,
            "cm_dir": res_dir,
            "protocol": "fallback",
        }
