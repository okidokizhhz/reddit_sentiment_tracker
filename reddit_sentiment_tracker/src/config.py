# reddit_sentiment_tracker/reddit_sentiment_tracker/src.config.py

from pathlib import Path

# current location of config.py acts as root
BASE_DIR = Path(__file__).resolve().parent
# Paths
TOP_POSTS_DATA_PATH = BASE_DIR / "data" / "top_posts_data.json"
# Path to save rising posts data
RISING_POSTS_DATA_PATH = BASE_DIR / "data" / "rising_posts_data.json"

# rate limits
RATE_LIMIT_TOP_POSTS = 5
RATE_LIMIT_RISING_POSTS = 5
COMMENT_LIMIT = 3
# Nested comments depth
REPLY_DEPTH = 1

# TIME FILTER
TOP_POSTS_TIME_FILTER = "week"
