import logging
from contextlib import contextmanager
from sqlalchemy.exc import SQLAlchemyError
from .connection import engine
from .schema_manager import subreddits, posts, comments, post_sentiment_history, comment_sentiment_history

logger = logging.getLogger("reddit_sentiment_tracker")


@contextmanager
def db_session():
    """ Context manager for transactions - begin() handles rollbacks/transactions """
    with engine.begin() as conn:
        try:
            yield conn
        except SQLAlchemyError as e:
            logger.error(f"Database Transaction failed: {e}", exc_info=True)
            raise   # error - let application entry point decide


def insert_subreddit_metadata(subreddit_metadata: dict):
    """ Inserting subreddit metadata into DB in a transaction """
    try:
        with db_session() as conn:
            conn.execute(subreddits.insert(), subreddit_metadata)

        logger.info(f"Successfully inserted subreddit metadata into DB")

    except Exception as e:
        logger.error(f"Failure inserting subreddit metadata into DB: {e}", exc_info=True)
        raise

def insert_top_posts(posts_data, subreddit_id):
    """ Inserting posts data into DB in a transaction """
    if not posts_data:
        logger.info("No posts data to insert")
        return

    posts_to_insert = []

    for post in posts_data:
        post_db_data = {
            "id": post["id"],
            "subreddit_id": subreddit_id,
            "author": post["author"],
            "post_type": "top",
            "title": post["title"],
            "selftext": post["selftext"],
            "url": post["url"],
            "flair": post["flair"],
            "created_utc": post["created_utc"]
        }
        posts_to_insert.append(post_db_data)

    try:
        with db_session() as conn:
            conn.execute(posts.insert(), posts_to_insert)

        logger.info(f"Successfully inserted posts data into DB")

    except Exception as e:
        logger.error(f"Failure inserting posts data into DB: {e}", exc_info=True)
        raise
