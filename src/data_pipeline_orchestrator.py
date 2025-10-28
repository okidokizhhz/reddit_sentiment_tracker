# ~/reddit_sentiment_tracker/src/data_pipeline_orchestrator.py

import sys
import logging
from typing import Any, Optional, Tuple, Dict, List
from .storage.connection import initialize_database
from .data_collection.reddit_client import get_reddit_client
from .data_collection.subreddit_fetcher import fetch_subreddit_metadata
from .storage.crud import insert_subreddit_metadata, insert_top_posts, insert_rising_posts, insert_comments, insert_post_sentiment, insert_comment_sentiment
from .data_collection.post_fetcher import fetch_top_posts, fetch_rising_posts
from .data_collection.comment_fetcher import fetch_comments

logger = logging.getLogger("reddit_sentiment_tracker")

def init_db() -> None:
    """ Initialize DB """
    try:
        initialize_database()
        logger.info("Database connection successful")
    except Exception as e:
        logger.critical(f"Failed to connect to DB: {e}. Exiting Program", exc_info=True)
        sys.exit(1)


def reddit_client() -> Optional[Any]:
    """ Retrieve Reddit Client """
    try:
        reddit = get_reddit_client()
        logger.info("Reddit Client retrieved successfully")
        return reddit
    except Exception as e:
        logger.fatal(f"Failed to retrieve Reddit client: {e}. Exiting Program", exc_info=True)
        sys.exit(1)         # Exit program on failure


def get_subreddit_metadata(subreddit_name: str, reddit: Any) -> Tuple[Dict[str, Any], str]:
    """ Fetch Subreddit Metadata """
    try:
        subreddit_metadata = fetch_subreddit_metadata(subreddit_name, reddit)
        if not subreddit_metadata or "id" not in subreddit_metadata:
            raise ValueError(f"Failed to fetch data for subreddit: '{subreddit_name}'")

        logger.info(f"Subreddit metadata of 'r/{subreddit_name}' fetched successfully")
        subreddit_id = subreddit_metadata["id"]
        return subreddit_metadata, subreddit_id

    except Exception as e:
        logger.error(f"Failed to fetch metadata of: r/{subreddit_name}: {e}", exc_info=True)
        raise


def subreddit_data_into_db(subreddit_name: str, subreddit_metadata: Dict[str, Any]) -> None:
    """ Insert Subreddit Metadata into Db """
    try:
        insert_subreddit_metadata(subreddit_metadata)
        logger.info(f"Subreddit metadata of 'r/{subreddit_name}' inserted into DB successfully")
    except Exception as e:
        logger.error(f"Failed to insert subreddit metadata of 'r/{subreddit_name}' into DB: {e}", exc_info=True)


def get_top_posts(subreddit_name: str, reddit: Any, RATE_LIMIT_TOP_POSTS: int, TOP_POSTS_TIME_FILTER: str) -> List[Dict[str, Any]]:
    """ Fetch Top Posts """
    try:
        top_posts_data = fetch_top_posts(subreddit_name,
                                         reddit,
                                         RATE_LIMIT_TOP_POSTS,
                                         TOP_POSTS_TIME_FILTER)
        if not top_posts_data:
            raise ValueError(f"Failed to fetch top posts data from the subreddit '{subreddit_name}'")

        return top_posts_data
    except Exception as e:
        logger.error(f"Failed to fetch top posts: {e}", exc_info=True)
        raise

def top_posts_data_into_db(top_posts_data: List[Dict[str, Any]], subreddit_id: str) -> None:
    """ Insert Top Posts Sentiment data into DB"""
    try:
        insert_top_posts(top_posts_data, subreddit_id)
        insert_post_sentiment(top_posts_data)

        logger.info("Inserting top posts and sentiment data into DB successful")
    except Exception as e:
        logger.error(f"Failed to insert top posts and sentiment data into DB: {e}", exc_info=True)


def comments_top_posts_into_db(top_posts_data: List[Dict[str, Any]], reddit: Any, REPLY_DEPTH: int, COMMENT_LIMIT: int) -> None:
    """ Insert Comments of top posts and and Sentiment into DB """
    try:
        for post in top_posts_data:
            post_id = post["id"]
            post["comments"] = fetch_comments(reddit,
                                              post_id,
                                              REPLY_DEPTH,
                                              COMMENT_LIMIT)
            post_comments = post["comments"]

            # DB: inserting comments of Top Posts
            try: 
                insert_comments(post_comments, post_id)
                insert_comment_sentiment(post_comments)

                logger.info(f"Post id {post_id}: Inserting comments and sentiments of Top Posts into DB successful")

            except Exception as e:
                logger.error(f"Post id {post_id}: Failed to insert comments and sentiments of Top Posts into DB: {e}", exc_info=True)
    except Exception as e:
        logger.error(f"Failed to fetch comments for Top Posts", exc_info=True)


def get_rising_posts(subreddit_name: str, reddit: Any, RATE_LIMIT_RISING_POSTS: int) -> List[Dict[str, Any]]:
    """ Fetch Rissing Posts """
    try:
        rising_posts_data = fetch_rising_posts(subreddit_name,
                                               reddit,
                                               RATE_LIMIT_RISING_POSTS)
        if not rising_posts_data:
            raise ValueError(f"Failed to fetch rising posts from the subreddit '{subreddit_name}'")

        return rising_posts_data
    except Exception as e:
        logger.error(f"failed to fetch rising posts: {e}", exc_info=True)
        raise


def rising_posts_data_into_db(rising_posts_data: List[Dict[str, Any]], subreddit_id: str) -> None:
    """ Inserting Rising Posts and Sentiment Data into DB """
    try: 
        insert_rising_posts(rising_posts_data, subreddit_id)
        insert_post_sentiment(rising_posts_data)

        logger.info("Inserting rising posts and sentiment data into DB successful")
    except Exception as e:
        logger.error(f"Failed to insert rising posts and sentiment data into DB: {e}", exc_info=True)


def comments_rising_posts_into_db(rising_posts_data: List[Dict[str, Any]], reddit: Any, REPLY_DEPTH: int, COMMENT_LIMIT: int) -> None:
    """ Insert Comments of rising posts and and Sentiment into DB """
    try:
        for post in rising_posts_data:
            post_id = post["id"]
            post["comments"] = fetch_comments(reddit,
                                              post["id"],
                                              REPLY_DEPTH,
                                              COMMENT_LIMIT)
            post_comments = post["comments"]

            # DB: inserting comments of Rising Posts
            try: 
                insert_comments(post_comments, post_id)
                insert_comment_sentiment(post_comments)

                logger.info(f"Post id {post_id}: Inserting comments and sentiments of Rising Posts into DB successful")

            except Exception as e:
                logger.error(f"Post id {post_id}: Failed to insert comments and sentiments of Rising Posts into DB: {e}", exc_info=True)


    except Exception as e:
        logger.error(f"Failed to fetch comments for Rising Posts", exc_info=True)
