# reddit_sentiment_tracker/reddit_sentiment_tracker/src.config.py

from pathlib import Path

# Root directory of the project
BASE_DIR = Path(__file__).resolve().parent

# Paths to various folders/files
FETCHED_DATA_PATH = BASE_DIR / "data" / "fetched_data.json"
