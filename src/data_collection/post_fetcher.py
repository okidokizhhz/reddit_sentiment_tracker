# ~/reddit_sentiment_tracker/src/data_collection/post_fetcher.py

import asyncpraw.exceptions
from .post_processor import process_post
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger("reddit_sentiment_tracker")

async def fetch_top_posts(subreddit_name: str, reddit: Any, RATE_LIMIT_TOP_POSTS: int, TOP_POSTS_TIME_FILTER: str) -> Optional[List[Dict[str, Any]]]:
    """ Fetches top posts from a Subreddit """
    try:
        subreddit = await reddit.subreddit(subreddit_name)           # accessing subreddit
        logger.info(f"Accessed the subreddit: {subreddit_name}")

        top_posts_data = []

        # fetching Top Posts data of subreddit
        async for post in subreddit.top(limit=RATE_LIMIT_TOP_POSTS,
                                  time_filter=TOP_POSTS_TIME_FILTER):
            top_posts_data.append(process_post(post))

        logger.info(f"Top Posts of subreddit '{subreddit_name}' fetched successfully")
        return top_posts_data 

    except asyncpraw.exceptions.APIException as e:
        logger.error(f"Reddit API Exception while fetching metadata for '{subreddit_name}': {e}")
        return None
    except Exception as e:
        logger.error(f"Error fetching '{subreddit_name}' data: {e}", exc_info=True)
        return None


async def fetch_rising_posts(subreddit_name: str, reddit: Any, RATE_LIMIT_RISING_POSTS: int) -> Optional[List[Dict[str, Any]]]:
    """ Fetches rising posts from a Subreddit """
    try:
        subreddit = await reddit.subreddit(subreddit_name)           # accessing subreddit
        logger.info(f"Accessed the subreddit: {subreddit_name}")

        rising_posts_data = []

        async for post in subreddit.rising(limit=RATE_LIMIT_RISING_POSTS):
            rising_posts_data.append(process_post(post))

        logger.info(f"Rising Posts of subreddit '{subreddit_name}' fetched successfully")
        return rising_posts_data 

    except asyncpraw.exceptions.APIException as e:
        logger.error(f"Reddit API Exception: {e}")
        return None
    except Exception as e:
        logger.error(f"Error fetching '{subreddit_name}' data: {e}", exc_info=True)
        return None
