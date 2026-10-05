"""
Package ews: Custom Early Warning System (EWS) v2.
"""

from ews.config import (
    DATA_PATHS,
    EWS_WEIGHTS,
    EWS_SCORE_LEVELS,
    INDOBERT_MODEL_METADATA,
)
from ews.emotion_analyzer import (
    load_emotion_data,
    get_emotion_distribution,
    get_emotion_percentages,
    get_dominant_emotion,
    get_emotion_risk,
)
from ews.sna_analyzer import (
    load_sna_data,
    get_top_degree,
    get_top_betweenness,
    get_communities,
    get_community_sizes,
    get_dominant_emotion_by_community,
    get_sna_summary,
)
from ews.anomaly_detector import (
    aggregate_daily_mentions,
    calculate_rolling_statistics,
    calculate_z_score,
    detect_spikes,
    get_anomaly_metrics,
)
from ews.keyword_analyzer import (
    extract_crisis_keywords,
    extract_emojis,
    extract_hashtags,
    get_keyword_risk,
)
from ews.ews_engine import (
    calculate_sarcasm_risk,
    compute_custom_ews_v2,
)
from ews.custom_dashboard import render_custom_ews

__all__ = [
    "DATA_PATHS",
    "EWS_WEIGHTS",
    "EWS_SCORE_LEVELS",
    "INDOBERT_MODEL_METADATA",
    "load_emotion_data",
    "get_emotion_distribution",
    "get_emotion_percentages",
    "get_dominant_emotion",
    "get_emotion_risk",
    "load_sna_data",
    "get_top_degree",
    "get_top_betweenness",
    "get_communities",
    "get_community_sizes",
    "get_dominant_emotion_by_community",
    "get_sna_summary",
    "aggregate_daily_mentions",
    "calculate_rolling_statistics",
    "calculate_z_score",
    "detect_spikes",
    "get_anomaly_metrics",
    "extract_crisis_keywords",
    "extract_emojis",
    "extract_hashtags",
    "get_keyword_risk",
    "calculate_sarcasm_risk",
    "compute_custom_ews_v2",
    "render_custom_ews",
]
