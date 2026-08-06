import os
import tempfile
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Compass Backend"
    VERSION: str = "1.0.0"
    
    GROQ_API_KEY: str = ""
    
    CHROMA_PATH: str = os.path.join(tempfile.gettempdir(), "compass_chroma_db")
    TEMP_DIR: str = os.path.join(tempfile.gettempdir(), "compass_temp")
    
    MAX_FILES: int = 500
    MAX_REPO_SIZE_MB: int = 100

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

# Ensure directories exist
os.makedirs(settings.TEMP_DIR, exist_ok=True)
os.makedirs(settings.CHROMA_PATH, exist_ok=True)
 
  