from fastapi import status, APIRouter
from fastapi.responses import RedirectResponse, JSONResponse
from starlette.requests import Request
from app.config import settings 
import urllib.parse
import requests
from requests.exceptions import RequestException
from datetime import datetime

router = APIRouter(tags=["authentication"])

def getUser(access_token: str):
    if not access_token:
        print("Error: Access token is missing")
        return None

    headers = {
        'Authorization': f"Bearer {access_token}"
    }

    try:
        response = requests.get(
            settings.API_BASE_URL + "me",
            headers=headers
        )

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            print(f"Error: Invalid token (Status {response.status_code}).")
            return None
        else:
            print(f"Error: Spotify API returned unexpected status {response.status_code}.")
            return None
    except RequestException as e:
        print(f"Network error while fetching user data: {e}")
        return None

def refresh_access_token(refresh_token: str):
    if not refresh_token:
        print("Error: refresh token is missing")
        return None
    
    req_body = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': settings.CLIENT_ID,
        'client_secret': settings.CLIENT_SECRET
    }

    try:
        response = requests.post(settings.TOKEN_URL, data=req_body)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            print(f"Error: Invalid refresh token (Status {response.status_code}).")
            return None
        else:
            print(f"Error: Spotify API returned unexpected status {response.status_code}.")
            return None
    except RequestException as e:
        print(f"Network error while fetching user data: {e}")
        return None

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

@router.get('/callback')
async def callback(code: str | None = None, error: str | None = None):
    if error:
        return JSONResponse({"error": error}, status_code=status.HTTP_400_BAD_REQUEST)
    
    if code:
        req_body = {
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': settings.REDIRECT_URI,
            'client_id': settings.CLIENT_ID,
            'client_secret': settings.CLIENT_SECRET
        }

        response = requests.post(settings.TOKEN_URL, data=req_body)

        if response.status_code != 200:
            return JSONResponse({"error": "Token exchange failed"}, status_code=response.status_code)
        
        token_info = response.json()

        # request.session['access_token'] = token_info.get('access_token')
        # request.session['refresh_token'] = token_info.get('refresh_token')
        # request.session['expires_at'] = datetime.now().timestamp() + token_info.get('expires_in')

        # print(request.session['access_token'])

        return JSONResponse(
            content={
                "message": "Token exchange succesfull",
                "access_token": token_info.get('access_token'),
                "refresh_token": token_info.get('refresh_token'),
                "expires_in": token_info.get('expires_in'),
                "token_type": token_info.get('token_type'),
            },
            status_code=status.HTTP_200_OK
        )