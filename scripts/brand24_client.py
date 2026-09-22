"""
brand24_client.py
=================
Brand24 API v1 client untuk riset MBG (Makan Bergizi Gratis).
Semua panggilan API dilakukan server-side; API Key TIDAK pernah dikirim ke frontend.

Account ID : 614604830
Docs       : https://api-data.brand24.com/api-data-docs/documentation
"""

import os
import json
import requests
from datetime import datetime, timedelta

# ────────────────────────────────────────────────
# KONFIGURASI
# ────────────────────────────────────────────────
ACCOUNT_ID = 614604830
BASE_URL    = "https://api-data.brand24.com/api-data/v1"
TIMEOUT     = 20   # detik


# ────────────────────────────────────────────────
# HELPER: Baca API Key
# ────────────────────────────────────────────────
def get_api_key() -> str | None:
    """Membaca API Key dari environment variable atau file .env."""
    # 1) env var langsung
    api_key = os.environ.get("BRAND24_API_KEY")
    if api_key and api_key != "your_brand24_api_key_here":
        return api_key.strip()

    # 2) file .env (cari dari direktori script, lalu project root)
    search_dirs = [
        os.path.dirname(os.path.abspath(__file__)),
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        os.getcwd(),
    ]
    for d in search_dirs:
        env_path = os.path.join(d, ".env")
        if os.path.exists(env_path):
            with open(env_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("BRAND24_API_KEY="):
                        val = line.split("=", 1)[1].strip().strip('"\'')
                        if val and val != "your_brand24_api_key_here":
                            return val
    return None


def _headers(api_key: str) -> dict:
    return {
        "X-Api-Key": api_key,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


def _get(url: str, api_key: str, params: dict = None) -> dict | None:
    """Generic GET wrapper dengan error handling."""
    try:
        r = requests.get(url, headers=_headers(api_key), params=params, timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error {r.status_code}: {r.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Gagal terhubung ke Brand24 API. Periksa koneksi internet.")
    except requests.exceptions.Timeout:
        print("❌ Request timeout (>20 detik). Coba lagi.")
    except Exception as e:
        print(f"❌ Error tidak terduga: {e}")
    return None


# ────────────────────────────────────────────────
# FUNGSI UTAMA
# ────────────────────────────────────────────────

def list_projects(api_key: str) -> dict | None:
    """
    Ambil daftar semua proyek monitoring di akun Brand24.
    Endpoint: GET /account/{account_id}/projects_list/
    """
    url = f"{BASE_URL}/account/{ACCOUNT_ID}/projects_list/"
    return _get(url, api_key)


def get_mentions(
    api_key: str,
    project_id: int,
    since_days: int = 7,
    max_results: int = 200,
    keyword: str = None,
) -> list[dict]:
    """
    Ambil mention terbaru dari proyek tertentu.
    Endpoint: GET /account/{account_id}/project/{project_id}/mentions/

    Args:
        since_days   : Rentang waktu mundur (hari).
        max_results  : Batas maksimum mention yang dikembalikan.
        keyword      : Filter opsional (kata kunci tambahan).
    Returns:
        List of mention dicts.
    """
    date_from = (datetime.utcnow() - timedelta(days=since_days)).strftime("%Y-%m-%dT%H:%M:%S")
    url = f"{BASE_URL}/account/{ACCOUNT_ID}/project/{project_id}/mentions/"
    params = {
        "date_from": date_from,
        "per_page": min(max_results, 100),  # API max 100/halaman
    }
    if keyword:
        params["q"] = keyword

    results = []
    page = 1
    while len(results) < max_results:
        params["page"] = page
        data = _get(url, api_key, params)
        if not data:
            break
        items = data.get("results", data.get("mentions", []))
        if not items:
            break
        results.extend(items)
        # Cek pagination
        next_url = data.get("next")
        if not next_url or len(results) >= max_results:
            break
        page += 1

    return results[:max_results]


def get_project_stats(api_key: str, project_id: int, since_days: int = 30) -> dict | None:
    """
    Ambil statistik agregat proyek (volume, sentiment, reach, dll).
    Endpoint: GET /account/{account_id}/project/{project_id}/stats/
    """
    date_from = (datetime.utcnow() - timedelta(days=since_days)).strftime("%Y-%m-%dT%H:%M:%S")
    url = f"{BASE_URL}/account/{ACCOUNT_ID}/project/{project_id}/stats/"
    return _get(url, api_key, params={"date_from": date_from})


def get_sentiment_breakdown(api_key: str, project_id: int, since_days: int = 30) -> dict | None:
    """
    Ambil breakdown sentimen (positif/negatif/netral) dari sebuah proyek.
    Endpoint: GET /account/{account_id}/project/{project_id}/sentiment/
    """
    date_from = (datetime.utcnow() - timedelta(days=since_days)).strftime("%Y-%m-%dT%H:%M:%S")
    url = f"{BASE_URL}/account/{ACCOUNT_ID}/project/{project_id}/sentiment/"
    return _get(url, api_key, params={"date_from": date_from})


def get_top_sources(api_key: str, project_id: int, since_days: int = 30) -> dict | None:
    """
    Ambil sumber media terpopuler (Twitter/X, Instagram, news, dll).
    Endpoint: GET /account/{account_id}/project/{project_id}/sources/
    """
    date_from = (datetime.utcnow() - timedelta(days=since_days)).strftime("%Y-%m-%dT%H:%M:%S")
    url = f"{BASE_URL}/account/{ACCOUNT_ID}/project/{project_id}/sources/"
    return _get(url, api_key, params={"date_from": date_from})


def get_authors(api_key: str, project_id: int, since_days: int = 30) -> dict | None:
    """
    Ambil data penulis/akun terpopuler yang menyebut kata kunci proyek.
    Endpoint: GET /account/{account_id}/project/{project_id}/authors/
    """
    date_from = (datetime.utcnow() - timedelta(days=since_days)).strftime("%Y-%m-%dT%H:%M:%S")
    url = f"{BASE_URL}/account/{ACCOUNT_ID}/project/{project_id}/authors/"
    return _get(url, api_key, params={"date_from": date_from})


# ────────────────────────────────────────────────
# EARLY WARNING SCORE (EWS)
# ────────────────────────────────────────────────

def compute_early_warning_score(stats: dict, sentiments: dict) -> dict:
    """
    Hitung skor Peringatan Dini (Early Warning Score / EWS) berbasis:
      - Volume mention (normalisasi 0–40 poin)
      - Rasio sentimen negatif (0–40 poin)
      - Velocity (lonjakan vs rata-rata) (0–20 poin)

    Returns dict dengan 'score' (0–100), 'level' (AMAN/WASPADA/BAHAYA/KRITIS),
    dan 'breakdown' per komponen.
    """
    total     = stats.get("total_mentions", 0) if stats else 0
    neg_count = sentiments.get("negative", 0)   if sentiments else 0
    pos_count = sentiments.get("positive", 0)   if sentiments else 0
    net_count = sentiments.get("neutral", 0)    if sentiments else 0
    total_sent = neg_count + pos_count + net_count or 1

    # Komponen 1: Volume (cap 500 mention → 40 poin)
    vol_score = min(total / 500 * 40, 40)

    # Komponen 2: Rasio negatif (100% negatif → 40 poin)
    neg_ratio = neg_count / total_sent
    neg_score = neg_ratio * 40

    # Komponen 3: Velocity placeholder (data series tidak tersedia via stats tunggal)
    vel_score = 0.0

    ews = vol_score + neg_score + vel_score

    if ews < 25:
        level = "🟢 AMAN"
    elif ews < 50:
        level = "🟡 WASPADA"
    elif ews < 75:
        level = "🟠 BAHAYA"
    else:
        level = "🔴 KRITIS"

    return {
        "score": round(ews, 1),
        "level": level,
        "breakdown": {
            "volume_score": round(vol_score, 1),
            "neg_sentiment_score": round(neg_score, 1),
            "velocity_score": round(vel_score, 1),
        },
        "raw": {
            "total_mentions": total,
            "negative": neg_count,
            "positive": pos_count,
            "neutral": net_count,
            "neg_ratio_pct": round(neg_ratio * 100, 1),
        }
    }


# ────────────────────────────────────────────────
# CLI — untuk testing langsung
# ────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    key = sys.argv[1] if len(sys.argv) > 1 else get_api_key()
    if not key:
        print("⚠️  API Key belum dikonfigurasi.")
        print("Cara penggunaan:")
        print("  python3 scripts/brand24_client.py <API_KEY>")
        print("  atau simpan di .env: BRAND24_API_KEY=your_key_here")
        sys.exit(1)

    print(f"🔌 Menghubungkan ke Brand24 API (Account ID: {ACCOUNT_ID})...")
    projects = list_projects(key)
    if not projects:
        print("❌ Gagal mengambil data proyek.")
        sys.exit(1)

    print(f"\n✅ Berhasil! Ditemukan {len(projects.get('results', projects))} proyek:")
    project_list = projects.get("results", projects if isinstance(projects, list) else [])
    for p in project_list:
        pid  = p.get("id") or p.get("project_id", "?")
        name = p.get("name") or p.get("keyword", "Tanpa Nama")
        print(f"   [{pid}] {name}")

    if project_list:
        first_id = project_list[0].get("id") or project_list[0].get("project_id")
        if first_id:
            print(f"\n📊 Mengambil stats proyek #{first_id}...")
            stats     = get_project_stats(key, first_id, since_days=30)
            sents     = get_sentiment_breakdown(key, first_id, since_days=30)
            ews       = compute_early_warning_score(stats, sents)
            print(f"\n🚨 Early Warning Score: {ews['score']}/100  →  {ews['level']}")
            print(json.dumps(ews['breakdown'], indent=2, ensure_ascii=False))
