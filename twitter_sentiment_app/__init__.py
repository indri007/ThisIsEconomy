"""
Twitter Sentiment Analysis Application package.
Provides modular components for scraping, text preprocessing, and sentiment analysis.
"""
import os
from pathlib import Path

__version__ = "1.0.0"


def get_secret(key_name: str, default: str = None) -> str:
    """Ambil key dari Streamlit Secrets (Cloud), .env (Lokal), atau .streamlit/secrets.toml."""
    try:
        import streamlit as st
        if hasattr(st, "secrets") and key_name in st.secrets:
            return str(st.secrets[key_name]).strip()
    except Exception:
        pass
    val = os.getenv(key_name, default)
    if val:
        return val.strip()

    # Fallback ke .streamlit/secrets.toml jika tersedia secara lokal
    secrets_path = Path(__file__).resolve().parent.parent / ".streamlit" / "secrets.toml"
    if secrets_path.exists():
        try:
            with open(secrets_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith(f"{key_name} =") or line.startswith(f"{key_name}="):
                        val = line.split("=", 1)[1].strip().strip('"').strip("'")
                        return val
        except Exception:
            pass

    return default
