from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import controllers/services
from services.sna_service import get_sna_summary, get_network_data
from services.emotion_service import get_emotion_distribution
from services.sarcasm_service import get_sarcasm_summary
from services.community_service import get_communities_summary

app = FastAPI(title="Tesis MBG API", description="Backend API for Tesis MBG Dashboard")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Tesis MBG API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/api/sna/summary")
def route_sna_summary():
    return get_sna_summary()

@app.get("/api/sna/network")
def route_network():
    return get_network_data()

@app.get("/api/emotion-distribution")
def route_emotion():
    return get_emotion_distribution()

@app.get("/api/sarcasm/summary")
def route_sarcasm():
    return get_sarcasm_summary()

@app.get("/api/sna/communities")
def route_communities():
    return get_communities_summary()

from services.hashtag_service import get_hashtag_summary, get_hashtag_network, get_emoji_summary, get_emoji_network

@app.get("/api/hashtag/summary")
def route_hashtag_summary():
    return get_hashtag_summary()

@app.get("/api/hashtag/network")
def route_hashtag_network():
    return get_hashtag_network()

@app.get("/api/emoji/summary")
def route_emoji_summary():
    return get_emoji_summary()

@app.get("/api/emoji/network")
def route_emoji_network():
    return get_emoji_network()

from services.explore_service import explore_hashtag, explore_emoji

@app.get("/api/explore/hashtag/{hashtag}")
def route_explore_hashtag(hashtag: str):
    return explore_hashtag(hashtag)

@app.get("/api/explore/emoji/{emoji_char}")
def route_explore_emoji(emoji_char: str):
    return explore_emoji(emoji_char)

from services.absa_service import get_absa_summary

@app.get("/api/absa/summary")
def route_absa_summary():
    return get_absa_summary()
