from fastapi import status, APIRouter
from fastapi.responses import RedirectResponse, JSONResponse
from starlette.requests import Request
from datetime import datetime
from app.utility.client import clientInit
from app.router.authentication import getUser, refresh_access_token
from app.config import settings 

import pandas as pd
import requests

router = APIRouter(tags=["recommendation"])

@router.get("/get-recommendation/{user_id}")
async def get_recommendation(user_id: str, request: Request):
    # Client initialization
    client = clientInit()
    db = client.spotify
    collection = db['track_history']

    # Get user data
    access_token = request.session.get('access_token')
    if not access_token:
        return JSONResponse(
            status_code=401,
            content={"message": "Authentication required. Access token missing."}
        )
    
    user_data = getUser(access_token)

    if user_data is None:
        return JSONResponse(
            status_code=403,
            content={"message": "User validation failed, Check token validity or network,"}
        )
    
    if user_data.get('id') != user_id:
        return JSONResponse(
            status_code=403,
            content={"message": "Forbidden access. Token ID does not match"}
        )

    query_filter = {"user_id": user_id}

    user_track_history = await collection.find_one(query_filter)
    user_track_history.pop('_id', None) 

    print(user_track_history)
    return JSONResponse(status_code=200, content=user_track_history)
