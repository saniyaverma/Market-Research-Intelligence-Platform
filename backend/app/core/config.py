from pathlib import Path
from dotenv import load_dotenv
import os

# backend/
BASE_DIR = Path(__file__).resolve().parents[2]

ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)

class Settings:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


settings = Settings()