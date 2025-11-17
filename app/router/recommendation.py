from fastapi import APIRouter
from fastapi.responses import JSONResponse
from starlette.requests import Request
from datetime import datetime
from app.utility.client import clientInit
from app.router.authentication import getUser, refresh_access_token
from app.config import settings 
from app.recommendation.recommendationEngine import recommendation_processor, user_preference

import requests

router = APIRouter(tags=["recommendation"])

@router.get("/get-recommendation/{user_id}")
async def get_recommendation(user_id: str, request: Request):
    # Client initialization
    client = clientInit()
    db = client.spotify
    collection = db['users']

    query_filter = {"user_id": user_id}

    # Get user's profile vector
    document = await collection.find_one(query_filter)

    songs = await recommendation_processor(document['profile_vector'])
    songs = songs.to_dict('records')

    return JSONResponse(
        content={
            "user_id": user_id,
            "recommendations": songs
        },
        status_code=200
    )

