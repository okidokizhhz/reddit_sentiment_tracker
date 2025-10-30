# reddit_sentiment_tracker/src.config.py

import os
from pathlib import Path

# current location of config.py acts as root
BASE_DIR = Path(__file__).resolve().parent.parent

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

# Redis Rate Limiting
REDIS_URL = os.getenv("REDIS_URL")
RATE_LIMIT_Redis = 10           # max requests allowed
WINDOW_SIZE_Redis = 60          # in seconds (time window duration)
