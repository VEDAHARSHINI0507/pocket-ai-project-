import os
from pathlib import Path
from dotenv import load_dotenv

# Calculate the path to the root directory where .env lives
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"

# Explicitly load from the absolute path
load_dotenv(dotenv_path=env_path)

APP_NAME = os.getenv("APP_NAME", "PocketSmart AI")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./pocketsmart.db")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY", "secret-key")

print("\n" + "="*50)
print(f"LOADING .ENV FROM: {env_path}")
print(f"DETECTED KEY: {GEMINI_API_KEY}")
print("="*50 + "\n")