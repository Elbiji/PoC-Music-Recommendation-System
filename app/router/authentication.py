from fastapi import APIRouter, Response
from fastapi.responses import RedirectResponse
from app.config import settings 
import urllib.parse
import requests

router = APIRouter(tags=["authentication"])

def getUser(access_token):
    headers = {
        'Authorization': f"Bearer {access_token}"
    }

    response = requests.get(
        settings.API_BASE_URL + "me",
        headers=headers
    )

    return response.json()

def refresh_access_token(refresh_token):
    req_body = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': settings.CLIENT_ID,
        'client_secret': settings.CLIENT_SECRET
    }
    
    response = requests.post(settings.TOKEN_URL, data=req_body)
    
    if response.status_code != 200:
        return None
    
    return response.json()

@router.get("/login")
async def login():
    scope = 'user-read-private user-read-email user-top-read user-read-recently-played'

    params = {
        'client_id': settings.CLIENT_ID,
        'response_type': 'code',
        'scope' : scope,
        'redirect_uri' : settings.REDIRECT_URI,
        'show_dialog' : True
    }

    auth_url = f"{settings.AUTH_URL}?{urllib.parse.urlencode(params)}"
    return RedirectResponse(auth_url)
