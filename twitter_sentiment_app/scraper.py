"""
Scraper tweet MBG (Makan Bergizi Gratis) menggunakan Twikit + Cookie Session Twitter/X.
Dioptimalkan untuk kompatibilitas Streamlit (Lokal & Streamlit Cloud) dan penanganan Rate Limit.
"""

import asyncio
import os
import json
import logging
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv

# Tangani event loop jika berjalan dalam konteks Streamlit
try:
    import nest_asyncio
    nest_asyncio.apply()
except Exception:
    # uvloop pada Python 3.14/uvicorn tidak perlu / tidak kompatibel dengan nest_asyncio
    pass

load_dotenv()
logger = logging.getLogger(__name__)

COOKIES_FILE = "cookies.json"


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


def init_twikit_client():
    """Inisialisasi Twikit client dengan cookies dari Streamlit Secrets / .env / cookies.json."""
    from twikit import Client
    client = Client(language="id-ID")

    auth_token = get_secret("TWITTER_AUTH_TOKEN")
    ct0 = get_secret("TWITTER_CT0")

    # 1. Prioritas utama: credentials langsung dari Streamlit Secrets atau .env
    if auth_token and ct0:
        client.set_cookies({
            "auth_token": auth_token,
            "ct0": ct0
        })
        return client

    # 2. Fallback: file cookies.json jika tersedia
    if os.path.exists(COOKIES_FILE):
        try:
            client.load_cookies(COOKIES_FILE)
            return client
        except Exception as e:
            logger.warning(f"Gagal memuat {COOKIES_FILE}: {e}")

    raise ValueError(
        "Autentikasi Twitter belum diset! Masukkan TWITTER_AUTH_TOKEN dan TWITTER_CT0 "
        "di Streamlit Cloud Secrets atau file .env lokal."
    )


async def scrape_tweets(
    keyword: str = 'MBG OR "Makan Bergizi Gratis"',
    limit: int = 100,
    product: str = "Latest",
) -> pd.DataFrame:
    """
    Scrape tweet berdasarkan keyword secara asinkron.
    product: "Latest" (terbaru) atau "Top" (paling populer)
    """
    client = init_twikit_client()

    try:
        tweets = await client.search_tweet(keyword, product=product)
    except Exception as e:
        logger.error(f"Gagal saat pencarian awal tweet: {e}")
        raise RuntimeError(f"Gagal mencari tweet: {e}")

    rows = []
    count = 0

    while tweets and count < limit:
        for t in tweets:
            if count >= limit:
                break

            tweet_text = getattr(t, "full_text", None) or getattr(t, "text", "")
            screen_name = getattr(getattr(t, "user", None), "screen_name", "unknown")

            rows.append({
                "tweet_id": str(getattr(t, "id", "")),
                "username": screen_name,
                "created_at": str(getattr(t, "created_at", "")),
                "text": tweet_text,
                "retweet_count": getattr(t, "retweet_count", 0),
                "favorite_count": getattr(t, "favorite_count", 0),
                "reply_count": getattr(t, "reply_count", 0),
                "lang": getattr(t, "lang", "id"),
                "url": f"https://x.com/{screen_name}/status/{getattr(t, 'id', '')}",
                "scraped_at": datetime.now().isoformat(),
            })
            count += 1

        if count >= limit:
            break

        # Jeda 2.5 detik antar request halaman untuk mencegah rate limit
        await asyncio.sleep(2.5)

        try:
            tweets = await tweets.next()
            if not tweets:
                break
        except Exception as err:
            logger.warning(f"Berhenti mengambil tweet lanjutan (mungkin rate limit): {err}")
            break

    return pd.DataFrame(rows)


def scrape_tweets_sync(
    keyword: str = 'MBG OR "Makan Bergizi Gratis"',
    limit: int = 100,
    product: str = "Latest",
) -> pd.DataFrame:
    """
    Wrapper sinkron yang aman dipanggil langsung dari thread Streamlit & uvloop.
    Dijalankan di thread terpisah agar memiliki event loop bersih.
    """
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(lambda: asyncio.run(scrape_tweets(keyword, limit, product)))
        return future.result()


if __name__ == "__main__":
    print("Memulai uji coba scraping 10 tweet...")
    try:
        df = scrape_tweets_sync(limit=10)
        print(f"Berhasil mengambil {len(df)} tweet:")
        print(df[["username", "text"]].head())
    except Exception as e:
        print(f"Error: {e}")
