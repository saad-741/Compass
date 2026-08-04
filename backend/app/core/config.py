import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Compass Backend"
    VERSION: str = "1.0.0"
    
    # Environment variables
    GROQ_API_KEY: str = ""
    CHROMA_PATH: str = "./app/vectorstore/chroma_db"
    TEMP_DIR: str = "./app/temp"
    MAX_FILES: int = 500
    MAX_REPO_SIZE_MB: int = 100

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

# Ensure critical directories exist on startup
os.makedirs(settings.TEMP_DIR, exist_ok=True)
os.makedirs(settings.CHROMA_PATH, exist_ok=True)