import os

from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)

class Settings:
    APP_NAME = "AI Engineering Copilot"
    APP_VERSION = "0.1.0"

    DATA_DIR = os.getenv(
        "DATA_DIR",
        "data/repositories"
    )

    EMBEDDING_MODEL = os.getenv(
        "EMBEDDING_MODEL",
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    GROQ_MODEL = os.getenv(
        "GROQ_MODEL",
        "openai/gpt-oss-20b"
    )


settings = Settings()