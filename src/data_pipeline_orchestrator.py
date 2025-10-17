# ~/reddit_sentiment_tracker/src/data_pipeline_orchestrator.py

import sys
import logging
from .storage.connection import initialize_database
from .data_collection.reddit_client import get_reddit_client
from .data_collection.subreddit_fetcher import fetch_subreddit_metadata
from .storage.crud import insert_subreddit_metadata, insert_top_posts, insert_rising_posts, insert_comments, insert_post_sentiment, insert_comment_sentiment
from .data_collection.post_fetcher import fetch_top_posts, fetch_rising_posts
from .data_collection.comment_fetcher import fetch_comments

logger = logging.getLogger("reddit_sentiment_tracker")

def init_db():
    """ Initialize DB """
    try:
        initialize_database()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.critical(f"Failed to initialize DB: {e}. Exiting Program", exc_info=True)
        sys.exit(1)


def reddit_client():
    """ Retrieve Reddit Client """
    try:
        reddit = get_reddit_client()
        logger.info("Reddit Client retrieved successfully")
        return reddit
    except Exception as e:
        logger.fatal(f"Failed to retrieve Reddit client: {e}. Exiting Program", exc_info=True)
        sys.exit(1)         # Exit program on failure


def get_subreddit_metadata(subreddit_name, reddit):
    """ Fetch Subreddit Metadata """
    try:
        subreddit_metadata = fetch_subreddit_metadata(subreddit_name, reddit)
        logger.info(f"Subreddit metadata of 'r/{subreddit_name}' fetched successfully")
        subreddit_id = subreddit_metadata["id"]
        return subreddit_metadata, subreddit_id
    except Exception as e:
        logger.error(f"Failed to fetch metadata of: r/{subreddit_name}: {e}", exc_info=True)
        return None, None


def subreddit_data_into_db(subreddit_name, subreddit_metadata):
    """ Insert Subreddit Metadata into Db """
    try:
        insert_subreddit_metadata(subreddit_metadata)
        logger.info(f"Subreddit metadata of 'r/{subreddit_name}' inserted into DB successfully")
    except Exception as e:
        logger.error(f"Failed to insert subreddit metadata of 'r/{subreddit_name}' into DB: {e}", exc_info=True)


def get_top_posts(subreddit_name, reddit, RATE_LIMIT_TOP_POSTS, TOP_POSTS_TIME_FILTER):
    """ Fetch Top Posts """
    try:
        top_posts_data = fetch_top_posts(subreddit_name,
                                         reddit,
                                         RATE_LIMIT_TOP_POSTS,
                                         TOP_POSTS_TIME_FILTER)
        return top_posts_data
    except Exception as e:
        logger.error(f"Failed to fetch top posts: {e}", exc_info=True)

def top_posts_data_into_db(top_posts_data, subreddit_id):
    """ Insert Top Posts Sentiment data into DB"""
    try:
        insert_top_posts(top_posts_data, subreddit_id)
        insert_post_sentiment(top_posts_data)

        logger.info("Inserting top posts and sentiment data into DB successful")
    except Exception as e:
        logger.error(f"Failed to insert top posts and sentiment data into DB: {e}", exc_info=True)


def comments_top_posts_into_db(top_posts_data, reddit, REPLY_DEPTH, COMMENT_LIMIT):
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


def get_rising_posts(subreddit_name, reddit, RATE_LIMIT_RISING_POSTS):
    """ Fetch Rissing Posts """
    try:
        rising_posts_data = fetch_rising_posts(subreddit_name,
                                               reddit,
                                               RATE_LIMIT_RISING_POSTS)
        return rising_posts_data
    except Exception as e:
        logger.error(f"failed to fetch rising posts: {e}", exc_info=True)


def rising_posts_data_into_db(rising_posts_data, subreddit_id):
    """ Inserting Rising Posts and Sentiment Data into DB """
    try: 
        insert_rising_posts(rising_posts_data, subreddit_id)
        insert_post_sentiment(rising_posts_data)

        logger.info("Inserting rising posts and sentiment data into DB successful")
    except Exception as e:
        logger.error(f"Failed to insert rising posts and sentiment data into DB: {e}", exc_info=True)


def comments_rising_posts_into_db(rising_posts_data, reddit, REPLY_DEPTH, COMMENT_LIMIT):
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
