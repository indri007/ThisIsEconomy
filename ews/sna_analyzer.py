"""
ews/sna_analyzer.py
===================
Modul Integrasi Social Network Analysis (SNA) untuk Custom EWS v2.
Mengekstraksi metrik sentralitas aktor (Degree, Betweenness), partisi komunitas,
dan emosi dominan per kelompok diskursus secara objektif dan netral.

BATASAN METODOLOGIS:
- Metrik sentralitas mencerminkan posisi struktural transmisi informasi,
  BUKAN indikator kausal kesalahan atau penyebab krisis.
- Menggunakan istilah analitis netral:
  * High-connectivity node / Broadcaster (Out-Degree tinggi)
  * Target sink / Information sink (In-Degree tinggi)
  * Network bridge / Information broker (Betweenness tinggi)
"""

from __future__ import annotations
from typing import Dict, Any, List
import pandas as pd
from ews.config import DATA_PATHS


def load_sna_data(filepath: str | None = None) -> pd.DataFrame:
    """
    Memuat dataset simpul jaringan (971 nodes, 342 komunitas).
    Default path: data/results/mbg_network_nodes_final.csv
    """
    path = filepath or DATA_PATHS["sna_nodes"]
    try:
        df = pd.read_csv(path)
        required_cols = {"Id", "Label", "Degree", "Betweenness", "Community", "Dominant_Emotion"}
        missing = required_cols - set(df.columns)
        if missing:
            raise ValueError(f"Kolom wajib tidak lengkap di {path}: {missing}")
        return df
    except Exception as exc:
        raise RuntimeError(f"Gagal memuat dataset SNA dari {path}: {exc}")


def get_top_degree(df: pd.DataFrame, n: int = 10) -> List[Dict[str, Any]]:
    """
    Mengambil top-n aktor dengan sentralitas konektivitas tertinggi (High-Connectivity Nodes).
    """
    top_df = df.nlargest(n, "Degree")[
        ["Id", "Label", "Degree", "Betweenness", "Community", "Dominant_Emotion"]
    ]
    return top_df.to_dict(orient="records")


def get_top_betweenness(df: pd.DataFrame, n: int = 10) -> List[Dict[str, Any]]:
    """
    Mengambil top-n aktor penjembatan informasi antar-kelompok (Network Bridges / Brokers).
    """
    top_df = df.nlargest(n, "Betweenness")[
        ["Id", "Label", "Degree", "Betweenness", "Community", "Dominant_Emotion"]
    ]
    return top_df.to_dict(orient="records")


def get_communities(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Menganalisis statistik partisi komunitas dalam jaringan MBG.
    """
    total_nodes = len(df)
    total_communities = df["Community"].nunique()
    
    return {
        "total_nodes": total_nodes,
        "total_communities": total_communities,
        "mean_community_size": round(total_nodes / total_communities, 2) if total_communities else 0.0,
    }


def get_community_sizes(df: pd.DataFrame, top_n: int = 10) -> List[Dict[str, Any]]:
    """
    Mendapatkan daftar komunitas terbesar berdasarkan jumlah simpul anggota.
    """
    comm_counts = df["Community"].value_counts().head(top_n).reset_index()
    comm_counts.columns = ["Community", "Node_Count"]
    
    # Tambahkan emosi dominan di komunitas tersebut
    results = []
    for _, row in comm_counts.iterrows():
        c_id = row["Community"]
        c_nodes = df[df["Community"] == c_id]
        dom_emo = c_nodes["Dominant_Emotion"].mode()[0] if not c_nodes["Dominant_Emotion"].empty else "unknown"
        results.append({
            "Community": int(c_id),
            "Node_Count": int(row["Node_Count"]),
            "Dominant_Emotion": dom_emo,
        })
    return results


def get_dominant_emotion_by_community(df: pd.DataFrame) -> Dict[str, int]:
    """
    Menghitung sebaran emosi dominan di seluruh 342 komunitas.
    """
    comm_emotions = df.groupby("Community")["Dominant_Emotion"].agg(
        lambda s: s.mode()[0] if not s.empty else "unknown"
    )
    return comm_emotions.value_counts().to_dict()


def get_sna_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Ringkasan terstruktur integrasi metrik SNA untuk dasbor EWS v2.
    """
    return {
        "communities_stat": get_communities(df),
        "top_degree_actors": get_top_degree(df, 10),
        "top_betweenness_bridges": get_top_betweenness(df, 10),
        "top_community_clusters": get_community_sizes(df, 10),
        "community_dominant_emotions": get_dominant_emotion_by_community(df),
    }
