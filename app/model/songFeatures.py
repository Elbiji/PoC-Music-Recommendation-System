import random
from pydantic import BaseModel
from typing import Literal

class AudioFeatures(BaseModel):
    danceability: float
    energy: float
    key: int
    loudness: float
    speechiness: float
    acousticness: float
    instrumentalness: float
    liveness: float
    valence: float
    tempo: int
    mode: Literal[0,1]

def generate_random_feature() -> AudioFeatures:
    audio_features = {
        "danceability": random.uniform(0.55,0.85),
        "energy": random.random(),
        "key": random.randint(0,11),
        "loudness": random.uniform(-12.0,-6.0),
        "speechiness": random.uniform(0.03,0.1),
        "acousticness": random.uniform(0.01,0.2),
        "instrumentalness": random.uniform(0.0, 0.5),
        "liveness": random.uniform(0.08,0.25),
        "valence": random.uniform(0.4, 0.8),
        "tempo": random.randint(90, 150),
        "mode": random.randint(0,1)
    }

    # Unpacking audio_features using double asterisk (**)
    return AudioFeatures(**audio_features)
