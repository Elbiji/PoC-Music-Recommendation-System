from pydantic_settings import BaseSettings, SettingsConfigDict
import os

'''
BaseSettings memperbolehkan suatu atribut pada kelas
agar diassign sebuah nilai dari .env
'''
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=os.path.join(os.path.dirname(__file__), '..', '.env'), env_file_encoding='utf-8')
    # model_config = SettingsConfigDict(env_file_encoding='utf-8')

    CLIENT_ID: str
    CLIENT_SECRET: str
    REDIRECT_URI: str
    AUTH_URL: str
    TOKEN_URL: str
    API_BASE_URL: str
    DATABASE_URI: str
    SECRET_KEY: str

settings = Settings()