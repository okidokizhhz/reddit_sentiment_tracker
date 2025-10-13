# ~/reddit_sentiment_tracker/src/data_collection/post_fetcher.py

import praw
import praw.exceptions
from .post_processor import process_post
import logging

logger = logging.getLogger("reddit_sentiment_tracker")

def fetch_top_posts(subreddit_name: str, reddit, RATE_LIMIT_TOP_POSTS: int, TOP_POSTS_TIME_FILTER: str) -> list:
    """ Fetches top posts from a Subreddit """
    try:
        subreddit = reddit.subreddit(subreddit_name)           # accessing subreddit
        logger.info(f"Accessed the subreddit: {subreddit_name}")
    except Exception as e:
        logger.error(f"Error accessing subreddit via Reddit Client: {e}", exc_info=True)

    top_posts_data = []

    # fetching Top Posts data of subreddit
    try:
        for post in subreddit.top(limit=RATE_LIMIT_TOP_POSTS,
                                  time_filter=TOP_POSTS_TIME_FILTER):
            top_posts_data.append(process_post(post))

        logger.info(f"Top Posts of subreddit '{subreddit_name}' fetched successfully")
        return top_posts_data 

    except praw.exceptions.APIException as e:
        logger.error(f"Reddit API Exception: {e}")
        return []
    except Exception as e:
        logger.error(f"Error fetching '{subreddit_name}' data: {e}", exc_info=True)
        return []

def fetch_rising_posts(subreddit_name: str, reddit, RATE_LIMIT_RISING_POSTS: int) -> list:
    """ Fetches rising posts from a Subreddit. """
    try:
        subreddit = reddit.subreddit(subreddit_name)           # accessing subreddit
        logger.info(f"Accessed the subreddit: {subreddit_name}")
    except Exception as e:
        logger.error(f"Error accessing subreddit: {e}", exc_info=True)

    rising_posts_data = []

    # fetching Rising Posts data of subreddit
    try:
        for post in subreddit.rising(limit=RATE_LIMIT_RISING_POSTS):
            rising_posts_data.append(process_post(post))

        logger.info(f"Rising Posts of subreddit '{subreddit_name}' fetched successfully")
        return rising_posts_data 

    except praw.exceptions.APIException as e:
        logger.error(f"Reddit API Exception: {e}")
        return []
    except Exception as e:
        logger.error(f"Error fetching '{subreddit_name}' data: {e}", exc_info=True)
        return []
