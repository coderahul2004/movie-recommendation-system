import os
import pickle
from typing import List, Tuple, Optional, Dict, Any

import numpy as np
import pandas as pd
import requests
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# =========================
# ENV
# =========================
load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")

if not OMDB_API_KEY:
    raise RuntimeError("OMDB_API_KEY missing. Add it in .env")

# =========================
# FASTAPI APP
# =========================
app = FastAPI(title="Movie Recommender API (OMDb)", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# LOAD FILES
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DF_PATH = os.path.join(BASE_DIR, "df.pkl")
INDICES_PATH = os.path.join(BASE_DIR, "indices.pkl")
TFIDF_MATRIX_PATH = os.path.join(BASE_DIR, "tfidf_matrix.pkl")

df: Optional[pd.DataFrame] = None
indices_obj: Any = None
tfidf_matrix: Any = None
TITLE_TO_IDX: Optional[Dict[str, int]] = None

# =========================
# HELPERS
# =========================
def normalize(title: str) -> str:
    return str(title).strip().lower()


def build_index_map(indices: Any) -> Dict[str, int]:
    mapping = {}
    for k, v in indices.items():
        mapping[normalize(k)] = int(v)
    return mapping


def get_index(title: str) -> int:
    key = normalize(title)
    if key not in TITLE_TO_IDX:
        raise HTTPException(status_code=404, detail="Movie not found")
    return TITLE_TO_IDX[key]


def tfidf_recommend(title: str, n: int = 10) -> List[Tuple[str, float]]:
    idx = get_index(title)

    qv = tfidf_matrix[idx]
    scores = (tfidf_matrix @ qv.T).toarray().ravel()

    order = np.argsort(-scores)

    results = []
    for i in order:
        if i == idx:
            continue
        movie_title = df.iloc[i]["title"]
        results.append((movie_title, float(scores[i])))
        if len(results) >= n:
            break

    return results


# =========================
# OMDb FUNCTION
# =========================
def get_movie_details(title: str):
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
    try:
        return requests.get(url).json()
    except:
        return {}


# =========================
# STARTUP
# =========================
@app.on_event("startup")
def load_data():
    global df, indices_obj, tfidf_matrix, TITLE_TO_IDX

    with open(DF_PATH, "rb") as f:
        df = pickle.load(f)

    with open(INDICES_PATH, "rb") as f:
        indices_obj = pickle.load(f)

    with open(TFIDF_MATRIX_PATH, "rb") as f:
        tfidf_matrix = pickle.load(f)

    TITLE_TO_IDX = build_index_map(indices_obj)


# =========================
# ROUTES
# =========================
@app.get("/")
def home():
    return {"message": "Movie Recommendation API running 🚀"}


@app.get("/recommend")
def recommend(title: str = Query(...), n: int = 10):
    recs = tfidf_recommend(title, n)

    output = []

    for movie_title, score in recs:
        data = get_movie_details(movie_title)

        output.append({
            "title": movie_title,
            "score": score,
            "poster": data.get("Poster"),
            "year": data.get("Year"),
            "rating": data.get("imdbRating")
        })

    return output