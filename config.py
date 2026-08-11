import os
from pathlib import Path
from dotenv import load_dotenv


# Project root folder
BASE_DIR = Path(__file__).resolve().parent

# Load .env from project root
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


TMDB_API_KEY = os.getenv("328a5fc5e4b2e3b13ea740e5ab77f8e1")


if TMDB_API_KEY:
    print("TMDB API key loaded successfully!")
else:
    print("TMDB API key not found!")