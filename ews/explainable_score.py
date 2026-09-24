
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import pandas as pd


@dataclass
class EWSResult:
    score: float
    status: str
    contributors: list
    text: str


def prepare(
    emotion_df: pd.DataFrame,
    sarcasm_df: pd.DataFrame | None = None,
) -> pd.DataFrame:

    df = emotion_df.copy()

    if "created_at" in df.columns:
        df["created_at"] = pd.to_datetime(
            df["created_at"],
            errors="coerce",
            utc=True,
        )

    if "predicted_emotion" not in df.columns:
        df["predicted_emotion"] = "Netral"

    if sarcasm_df is not None and "id" in df.columns and "id" in sarcasm_df.columns:
        sar = sarcasm_df[["id", "sindiran"]].copy()
        sar = sar.drop_duplicates("id")

        df = df.merge(
            sar,
            on="id",
            how="left",
        )

    else:
        df["sindiran"] = None

    return df


def build_context(
    df: pd.DataFrame,
    nodes: pd.DataFrame | None = None,
) -> dict:

    context = {
        "tweets": len(df),
        "emotion": {},
        "sarcasm": {},
        "nodes": 0,
        "communities": 0,
    }

    if "predicted_emotion" in df.columns:
        context["emotion"] = (
            df["predicted_emotion"]
            .fillna("Netral")
            .value_counts()
            .to_dict()
        )

    if "sindiran" in df.columns:
        context["sarcasm"] = (
            df["sindiran"]
            .fillna("")
            .astype(str)
            .value_counts()
            .to_dict()
        )

    if nodes is not None and not nodes.empty:
        context["nodes"] = len(nodes)

        if "Community" in nodes.columns:
            context["communities"] = (
                nodes["Community"].nunique()
            )

    return context


def calculate_score(context: dict) -> EWSResult:

    contributors = []

    total = max(
        int(context.get("tweets", 0)),
        1,
    )

    emotion = context.get(
        "emotion",
        {},
    )

    sarcasm = context.get(
        "sarcasm",
        {},
    )

    # --------------------------------------------------
    # Emotion signal
    # --------------------------------------------------

    risk_emotions = {
        "Marah",
        "Jijik",
        "Takut",
        "Sedih",
    }

    risk_count = sum(
        int(emotion.get(label, 0))
        for label in risk_emotions
    )

    emotion_pct = (
        risk_count / total * 100
    )

    emotion_score = min(
        emotion_pct,
        30,
    )

    if emotion_score > 0:
        contributors.append({
            "component": "Emotion",
            "score": round(emotion_score, 2),
            "reason": (
                f"{emotion_pct:.2f}% "
                "tweet berada pada kelompok emotion "
                "yang digunakan sebagai risk signal."
            ),
        })

    # --------------------------------------------------
    # Sarcasm signal
    # --------------------------------------------------

    sarcasm_count = 0

    for label, count in sarcasm.items():

        normalized = str(label).lower()

        if normalized in {
            "1",
            "true",
            "yes",
            "sarkasme",
            "sindiran",
            "sarcastic",
        }:
            sarcasm_count += int(count)

    sarcasm_pct = (
        sarcasm_count / total * 100
    )

    sarcasm_score = min(
        sarcasm_pct * 0.20,
        20,
    )

    if sarcasm_score > 0:
        contributors.append({
            "component": "Sarcasm",
            "score": round(sarcasm_score, 2),
            "reason": (
                f"sarcasm signal {sarcasm_pct:.2f}% "
                "berdasarkan label dataset."
            ),
        })

    # --------------------------------------------------
    # Network signal
    # --------------------------------------------------

    network_score = 0

    if context.get("nodes", 0) > 0:
        network_score = min(
            context["nodes"] / 100,
            10,
        )

        contributors.append({
            "component": "SNA",
            "score": round(network_score, 2),
            "reason": (
                f"{context['nodes']} network nodes "
                "tersedia sebagai konteks struktur jaringan."
            ),
        })

    # --------------------------------------------------
    # Final
    # --------------------------------------------------

    score = min(
        100,
        emotion_score
        + sarcasm_score
        + network_score,
    )

    if score >= 75:
        status = "CRITICAL"
    elif score >= 50:
        status = "DANGER"
    elif score >= 25:
        status = "WARNING"
    else:
        status = "SAFE"

    contributors.sort(
        key=lambda x: x["score"],
        reverse=True,
    )

    text = (
        f"EWS SCORE: {score:.2f}\n"
        f"STATUS: {status}\n\n"
        "CONTRIBUTORS:\n"
    )

    for item in contributors:
        text += (
            f"- {item['component']}: "
            f"{item['score']:.2f}\n"
            f"  {item['reason']}\n"
        )

    return EWSResult(
        score=round(score, 2),
        status=status,
        contributors=contributors,
        text=text,
    )


def replay(
    context: dict,
    start: str,
    end: str,
) -> EWSResult:

    result = calculate_score(context)

    result.text = (
        f"HISTORICAL EWS REPLAY\n"
        f"PERIOD: {start} → {end}\n\n"
        + result.text
        + "\nNOTE: historical dataset; bukan live monitoring."
    )

    return result


def main():

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--emotion",
        default="data/results/indobert_9_emosi_fixed.csv",
    )

    parser.add_argument(
        "--sarcasm",
        default="data/sarcasm/dataset_sindiran_valid.csv",
    )

    parser.add_argument(
        "--nodes",
        default="data/results/mbg_network_nodes_final.csv",
    )

    parser.add_argument(
        "--start",
        required=True,
    )

    parser.add_argument(
        "--end",
        required=True,
    )

    args = parser.parse_args()

    emotion = pd.read_csv(
        args.emotion,
        dtype=str,
    )

    try:
        sarcasm = pd.read_csv(
            args.sarcasm,
            dtype=str,
        )
    except FileNotFoundError:
        sarcasm = None

    try:
        nodes = pd.read_csv(
            args.nodes,
        )
    except FileNotFoundError:
        nodes = None

    df = prepare(
        emotion,
        sarcasm,
    )

    start = pd.Timestamp(
        args.start,
        tz="UTC",
    )

    end = (
        pd.Timestamp(args.end, tz="UTC")
        + pd.Timedelta(days=1)
    )

    if "created_at" in df.columns:
        period_df = df[
            (df["created_at"] >= start)
            & (df["created_at"] < end)
        ].copy()
    else:
        period_df = df.copy()

    result = replay(
        build_context(
            period_df,
            nodes,
        ),
        args.start,
        args.end,
    )

    print(result.text)


if __name__ == "__main__":
    main()
