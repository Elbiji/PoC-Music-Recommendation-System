from pymongo import AsyncMongoClient
from pymongo.server_api import ServerApi
from app.config import settings

def clientInit():
    client = AsyncMongoClient(settings.DATABASE_URI, server_api=ServerApi('1'))
    return client