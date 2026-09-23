"""
Analisis sentimen + deteksi sarkasme tweet MBG menggunakan Google Gemini API.
Mendukung Streamlit Secrets (Cloud) dan .env (Lokal), dilengkapi retry tahan 429/503.
"""

import os
import time
import json
import logging
import pandas as pd
from google import genai
from google.genai import types
from google.genai.errors import APIError
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


def get_secret(key_name: str, default: str = None) -> str:
    """Ambil key dari Streamlit Secrets (Cloud) atau fallback ke .env (Lokal)."""
    try:
        import streamlit as st
        if hasattr(st, "secrets") and key_name in st.secrets:
            return str(st.secrets[key_name]).strip()
    except Exception:
        pass
    val = os.getenv(key_name, default)
    return val.strip() if val else None


SYSTEM_PROMPT = """Kamu adalah annotator ahli analisis sentimen dan sarkasme
dalam Bahasa Indonesia, khusus topik program pemerintah "Makan Bergizi Gratis" (MBG).

Untuk setiap tweet yang diberikan, tentukan:
1. sentiment: salah satu dari "positif", "negatif", "netral" (huruf kecil semua)
2. is_sarcasm: true/false (apakah tweet mengandung sarkasme/sindiran/ironi)
3. sentiment_if_sarcasm_removed: sentimen harfiah tweet jika sarkasme diabaikan
4. topic_aspect: pilih salah satu -- "kualitas makanan", "distribusi/logistik", "anggaran/korupsi", "kebijakan umum", "dampak kesehatan", "lainnya"
5. reason: alasan singkat (maksimal 15 kata) dalam Bahasa Indonesia

Output HARUS berupa JSON Array murni berisi list objek:
[
  {
    "sentiment": "negatif",
    "is_sarcasm": true,
    "sentiment_if_sarcasm_removed": "positif",
    "topic_aspect": "kualitas makanan",
    "reason": "Menyindir menu makanan yang kurang layak dengan kata pujian"
  }
]
Jangan tambahkan teks pembuka atau penutup markdown."""


def get_client(api_key: str = None) -> genai.Client:
    key = api_key or get_secret("GEMINI_API_KEY")
    if not key:
        raise ValueError(
            "GEMINI_API_KEY tidak ditemukan! Masukkan API key di sidebar atau file .env / Secrets."
        )
    return genai.Client(api_key=key.strip())


def parse_llm_json(raw_text: str) -> list[dict]:
    """Parse output LLM secara aman, membersihkan markdown code fence jika ada."""
    if not raw_text:
        return []

    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()

    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError:
        return []

    if isinstance(parsed, dict):
        for val in parsed.values():
            if isinstance(val, list):
                return val
        return [parsed]
    elif isinstance(parsed, list):
        return parsed

    return []


def analyze_batch(client: genai.Client, texts: list[str], max_retries: int = 3) -> list[dict]:
    """
    Analisis sekumpulan tweet (batch) dengan proteksi Exponential Backoff Retry.
    """
    model_name = get_secret("GEMINI_MODEL", "gemini-2.5-flash")
    numbered = "\n".join(f"{i+1}. {t}" for i, t in enumerate(texts))
    prompt = f"Analisis {len(texts)} tweet berikut:\n\n{numbered}"

    results = []
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    response_mime_type="application/json",
                    temperature=0.1,
                ),
            )
            raw_text = response.text or ""
            parsed = parse_llm_json(raw_text)

            if parsed and len(parsed) > 0:
                results = parsed
                break
            else:
                logger.warning(f"Percobaan {attempt+1}: Format JSON kosong, mencoba ulang...")
        except APIError as e:
            wait_time = (attempt + 1) * 4
            logger.warning(f"API Error ({e.code}): Tunggu {wait_time} detik...")
            time.sleep(wait_time)
        except Exception as e:
            logger.warning(f"Error tak terduga ({e}): Mencoba ulang...")
            time.sleep(3)

    cleaned_results = []
    for i in range(len(texts)):
        if i < len(results) and isinstance(results[i], dict):
            item = results[i]
            cleaned_results.append({
                "sentiment": str(item.get("sentiment", "netral")).lower().strip(),
                "is_sarcasm": bool(item.get("is_sarcasm", False)),
                "sentiment_if_sarcasm_removed": str(item.get("sentiment_if_sarcasm_removed", "netral")).lower().strip(),
                "topic_aspect": str(item.get("topic_aspect", "lainnya")).strip(),
                "reason": str(item.get("reason", "analisis selesai")),
            })
        else:
            cleaned_results.append({
                "sentiment": "netral",
                "is_sarcasm": False,
                "sentiment_if_sarcasm_removed": "netral",
                "topic_aspect": "lainnya",
                "reason": "gagal_analisis_api",
            })

    return cleaned_results


def analyze_dataframe(
    df: pd.DataFrame,
    text_col: str = "text",
    batch_size: int = 10,
    delay_seconds: float = 3.0,
    progress_callback=None,
    api_key: str = None,
) -> pd.DataFrame:
    """
    Analisis seluruh DataFrame tweet per-batch dengan jeda untuk menjaga kuota RPM.
    """
    client = get_client(api_key=api_key)
    all_results = []
    texts = df[text_col].fillna("").astype(str).tolist()
    total_batches = (len(texts) + batch_size - 1) // batch_size

    for idx, i in enumerate(range(0, len(texts), batch_size)):
        batch = texts[i : i + batch_size]
        batch_results = analyze_batch(client, batch)
        all_results.extend(batch_results)

        if progress_callback:
            progress_callback((idx + 1) / total_batches)

        if i + batch_size < len(texts):
            time.sleep(delay_seconds)

    result_df = pd.DataFrame(all_results)
    return pd.concat([df.reset_index(drop=True), result_df.reset_index(drop=True)], axis=1)


if __name__ == "__main__":
    test_df = pd.DataFrame({
        "username": ["andi", "budi"],
        "text": [
            "Luar biasa program makan gratis ini, menunya sehat dan bergizi untuk anak sekolah.",
            "Katanya anggaran ratusan triliun, tapi menunya cuma nasi sama kerupuk doang haha mantap!"
        ]
    })
    try:
        res = analyze_dataframe(test_df, batch_size=2)
        print(res[["text", "sentiment", "is_sarcasm", "reason"]])
    except Exception as e:
        print(f"Error: {e}")
