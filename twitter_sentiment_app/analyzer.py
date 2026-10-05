"""
Analisis sentimen + deteksi sarkasme tweet MBG menggunakan Google Gemini API.
Mendukung Streamlit Secrets (Cloud) dan .env (Lokal), dilengkapi retry tahan 429/503.
"""

from __future__ import annotations
import os
import time
import json
import logging
from typing import Any
import pandas as pd
try:
    from google import genai
    from google.genai import types
    from google.genai.errors import APIError
    GENAI_AVAILABLE = True
except (ImportError, AttributeError):
    genai = None
    types = None
    APIError = Exception
    GENAI_AVAILABLE = False
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
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


def parse_api_keys(api_keys_input: Any = None) -> list[str]:
    """
    Ekstrak daftar API Key dari berbagai sumber:
    1. Input langsung (UI/parameter: string tunggal, koma, newline, atau list)
    2. Jika kosong, fallback ke Streamlit Secrets (GEMINI_API_KEYS / GEMINI_API_KEY)
    3. Jika masih kosong, fallback ke .env (GEMINI_API_KEYS / GEMINI_API_KEY)
    """
    raw_candidates = []
    if api_keys_input:
        if isinstance(api_keys_input, (list, tuple, set)):
            raw_candidates.extend(api_keys_input)
        elif isinstance(api_keys_input, str):
            parts = [p.strip() for p in api_keys_input.replace("\r", "\n").replace(";", ",").split("\n")]
            for part in parts:
                raw_candidates.extend(part.split(","))

    # Jika belum ada input eksplisit, ambil dari Streamlit Secrets
    if not raw_candidates:
        try:
            import streamlit as st
            if hasattr(st, "secrets"):
                if "GEMINI_API_KEYS" in st.secrets:
                    val = st.secrets["GEMINI_API_KEYS"]
                    if isinstance(val, (list, tuple)):
                        raw_candidates.extend(val)
                    elif isinstance(val, str):
                        raw_candidates.extend(val.replace(";", ",").split(","))
                if "GEMINI_API_KEY" in st.secrets:
                    val = st.secrets["GEMINI_API_KEY"]
                    if isinstance(val, (list, tuple)):
                        raw_candidates.extend(val)
                    elif isinstance(val, str):
                        raw_candidates.extend(val.replace(";", ",").split(","))
        except Exception:
            pass

    # Jika masih belum ada, ambil dari os.getenv (.env)
    if not raw_candidates:
        for env_var in ("GEMINI_API_KEYS", "GEMINI_API_KEY"):
            val = os.getenv(env_var)
            if val:
                raw_candidates.extend(val.replace(";", ",").split(","))

    # Bersihkan whitespace, quote, deduplikasi dengan menjaga urutan
    cleaned = []
    seen = set()
    for k in raw_candidates:
        if not k:
            continue
        k_clean = str(k).strip().strip("'\"").strip()
        if k_clean and k_clean not in seen:
            seen.add(k_clean)
            cleaned.append(k_clean)

    return cleaned



class GeminiKeyPool:
    """
    Manajemen pool multi-key dengan auto-failover / rotasi dinamis jika kuota habis (429),
    error server sementara (503), atau kendala hak akses (403).
    """
    def __init__(self, keys: list[str] | None = None):
        self.keys = keys or []
        self.current_idx = 0

    def has_keys(self) -> bool:
        return len(self.keys) > 0

    def get_current_key(self) -> str:
        if not self.keys:
            raise ValueError(
                "GEMINI_API_KEY tidak ditemukan! Masukkan API key di sidebar atau file .env / Secrets."
            )
        return self.keys[self.current_idx]

    def rotate_key(self, reason: str = "") -> str:
        if len(self.keys) <= 1:
            return self.get_current_key()
        prev_key = self.keys[self.current_idx]
        masked_prev = f"{prev_key[:8]}...{prev_key[-4:]}" if len(prev_key) > 12 else prev_key
        self.current_idx = (self.current_idx + 1) % len(self.keys)
        new_key = self.keys[self.current_idx]
        masked_new = f"{new_key[:8]}...{new_key[-4:]}" if len(new_key) > 12 else new_key
        logger.warning(
            f"🔄 Rotasi API Key aktif: {masked_prev} ➡️ {masked_new} (Key {self.current_idx + 1}/{len(self.keys)}). Alasan: {reason}"
        )
        return new_key

    def get_client(self) -> Any:
        if not GENAI_AVAILABLE or genai is None:
            raise ImportError(
                "Paket 'google-genai' belum terpasang. Jalankan: pip install google-genai"
            )
        return genai.Client(api_key=self.get_current_key())


def get_client(api_key: str = None) -> Any:
    pool = GeminiKeyPool(parse_api_keys(api_key))
    return pool.get_client()


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


def analyze_batch(
    client: Any,
    texts: list[str],
    max_retries: int = 3,
    key_pool: GeminiKeyPool | None = None,
) -> list[dict]:
    """
    Analisis sekumpulan tweet (batch) dengan proteksi Exponential Backoff Retry,
    fallback model otomatis (mengatasi 404 model lama), dan rotasi multi-key failover.
    """
    # Model default yang terverifikasi aktif & stabil
    configured_model = get_secret("GEMINI_MODEL", "gemini-flash-latest")
    candidate_models = [configured_model, "gemini-flash-latest", "gemini-3.8-flash", "gemini-2.5-flash-lite"]
    # Deduplicate candidate models
    seen_m = set()
    model_queue = [m for m in candidate_models if m and not (m in seen_m or seen_m.add(m))]

    numbered = "\n".join(f"{i+1}. {t}" for i, t in enumerate(texts))
    prompt = f"Analisis {len(texts)} tweet berikut:\n\n{numbered}"

    results = []
    current_client = client
    model_idx = 0
    total_keys = len(key_pool.keys) if key_pool and key_pool.has_keys() else 1
    max_attempts = max(max_retries, total_keys + 1)

    for attempt in range(max_attempts):
        active_model = model_queue[model_idx % len(model_queue)]
        try:
            response = current_client.models.generate_content(
                model=active_model,
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
            err_msg = str(e)
            logger.warning(f"API Error ({getattr(e, 'code', 'NA')}): {err_msg[:120]}")
            # Jika model 404 (deprecated), ganti ke model kandidat berikutnya
            if "404" in err_msg or "NOT_FOUND" in err_msg or "no longer available" in err_msg:
                model_idx += 1
                logger.info(f"Model dialihkan ke: {model_queue[model_idx % len(model_queue)]}")
                continue

            # Jika kuota habis (429), server sibuk (503), atau izin ditolak (403): rotasi key jika ada pool
            if key_pool and len(key_pool.keys) > 1:
                key_pool.rotate_key(reason=f"API error code {getattr(e, 'code', 'NA')}")
                try:
                    current_client = key_pool.get_client()
                except Exception:
                    pass
                time.sleep(1)
                continue

            wait_time = min((attempt + 1) * 3, 10)
            logger.warning(f"Tunggu {wait_time} detik sebelum coba lagi...")
            time.sleep(wait_time)
        except Exception as e:
            err_msg = str(e)
            logger.warning(f"Error ({type(e).__name__}): {err_msg[:120]}")
            if key_pool and len(key_pool.keys) > 1 and ("429" in err_msg or "503" in err_msg or "403" in err_msg):
                key_pool.rotate_key(reason=err_msg[:60])
                try:
                    current_client = key_pool.get_client()
                except Exception:
                    pass
                time.sleep(1)
                continue
            time.sleep(2)

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
    delay_seconds: float = 2.0,
    progress_callback=None,
    api_key: Any = None,
) -> pd.DataFrame:
    """
    Analisis seluruh DataFrame tweet per-batch dengan dukungan multi-key pool,
    rotasi otomatis, dan jeda RPM dinamis.
    """
    keys = parse_api_keys(api_key)
    if not keys:
        raise ValueError(
            "GEMINI_API_KEY tidak ditemukan! Masukkan API key di sidebar atau file .env / Secrets."
        )

    key_pool = GeminiKeyPool(keys)
    client = key_pool.get_client()

    all_results = []
    texts = df[text_col].fillna("").astype(str).tolist()
    total_batches = (len(texts) + batch_size - 1) // batch_size

    for idx, i in enumerate(range(0, len(texts), batch_size)):
        batch = texts[i : i + batch_size]
        batch_results = analyze_batch(client, batch, key_pool=key_pool)
        all_results.extend(batch_results)

        # Selalu perbarui client aktif jika key_pool telah mengalami rotasi
        client = key_pool.get_client()

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
