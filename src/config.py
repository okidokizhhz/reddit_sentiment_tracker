# reddit_sentiment_tracker/src.config.py

from pathlib import Path

# current location of config.py acts as root
BASE_DIR = Path(__file__).resolve().parent.parent

# top posts path
TOP_POSTS_DATA_PATH = BASE_DIR / "fetched_posts" / "top_posts_data.json"
# rising posts path
RISING_POSTS_DATA_PATH = BASE_DIR / "fetched_posts" / "rising_posts_data.json"
# log path
LOG_DIR = BASE_DIR / "logs"

# rate limits
RATE_LIMIT_TOP_POSTS = 10
RATE_LIMIT_RISING_POSTS = 10
COMMENT_LIMIT = 3
# Nested comments depth
REPLY_DEPTH = 1

# TIME FILTER
TOP_POSTS_TIME_FILTER = "all"
