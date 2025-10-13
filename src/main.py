# ~/reddit_sentiment_tracker/src/main.py

import sys
from .data_collection.reddit_client import get_reddit_client
from .data_collection.post_fetcher import fetch_top_posts, fetch_rising_posts
from .data_collection.comment_fetcher import fetch_comments
from .config import TOP_POSTS_DATA_PATH, RISING_POSTS_DATA_PATH, RATE_LIMIT_RISING_POSTS, RATE_LIMIT_TOP_POSTS, COMMENT_LIMIT, TOP_POSTS_TIME_FILTER, REPLY_DEPTH
from .logger import setup_logger

logger = setup_logger("reddit_sentiment_tracker")

def main():
    try:
        reddit = get_reddit_client()
    except Exception as e:
        logger.fatal(f"Failed to retrieve Reddit client. Exiting Program: {e}", exc_info=True)
        sys.exit(1)         # Exit program on failure

    top_posts_data = fetch_top_posts("wien",
                                     reddit,
                                     RATE_LIMIT_TOP_POSTS,
                                     TOP_POSTS_TIME_FILTER)

    for post in top_posts_data:
        post_id = post["id"]
        post["comments"] = fetch_comments(reddit,
                                          post_id,
                                          REPLY_DEPTH,
                                          COMMENT_LIMIT)

    rising_posts_data = fetch_rising_posts("wien",
                                           reddit,
                                           RATE_LIMIT_RISING_POSTS)

    for post in rising_posts_data:
        post["comments"] = fetch_comments(reddit,
                                          post["id"],
                                          REPLY_DEPTH,
                                          COMMENT_LIMIT)

# SAVING
    # posts
    save_to_json(top_posts_data,
                 TOP_POSTS_DATA_PATH)
    save_to_json(rising_posts_data,
                 RISING_POSTS_DATA_PATH)

if __name__ == "__main__":
    main()
