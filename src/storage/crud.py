import logging
from contextlib import contextmanager
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from typing import Optional, Dict, Any
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
    if not subreddit_metadata:
        logger.info("No subreddit metadata to insert")
        return

    try:
        with db_session() as conn:
            # checking if subreddit already exists
            exists = conn.execute(
                select(subreddits.c.id).where(subreddits.c.id == subreddit_metadata["id"])
            ).fetchone()

            if exists:
                logger.info(f"The Subreddit '{subreddit_metadata["id"]}' already exists. Skipped inserting")
                return

            # otherwise insert
            conn.execute(subreddits.insert(), subreddit_metadata)

            logger.info(f"Successfully inserted subreddit metadata into DB")

    except Exception as e:
        logger.error(f"Failure inserting subreddit metadata into DB: {e}", exc_info=True)
        raise

def insert_top_posts(top_posts_data, subreddit_id):
    """ Inserting posts data into DB in a transaction """
    if not top_posts_data:
        logger.info("No posts data to insert")
        return

    try:
        with db_session() as conn:
            # getting post_id for each iteration
            for post in top_posts_data:
                post_id = post["id"]

                # check if post already exists
                exists = conn.execute(
                    select(posts.c.id).where(posts.c.id == post_id)
                ).fetchone()

                # return if duplicate
                if exists:
                    logger.info(f"The Post ID: '{post_id}' already exists. Skipped inserting")
                    continue

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

                # otherwise insert
                conn.execute(posts.insert(), post_db_data)

            logger.info(f"Successfully inserted new top posts into DB (duplicates skipped)")

    except Exception as e:
        logger.error(f"Failure inserting posts data into DB: {e}", exc_info=True)
        raise

def insert_rising_posts(rising_posts_data, subreddit_id):
    """ Inserting rising posts data into DB in a transaction """
    if not rising_posts_data:
        logger.info("No posts data to insert")
        return

    try:
        with db_session() as conn:
            for post in rising_posts_data:
                post_id = post["id"]

                # check if post already exists
                exists = conn.execute(
                    select(posts.c.id).where(posts.c.id == post_id)
                ).fetchone()

                # continue iterations if duplicate
                if exists:
                    logger.info(f"The Post ID: '{post_id}' already exists. Skipped inserting")
                    continue

                post_db_data = {
                    "id": post["id"],
                    "subreddit_id": subreddit_id,
                    "author": post["author"],
                    "post_type": "rising",
                    "title": post["title"],
                    "selftext": post["selftext"],
                    "url": post["url"],
                    "flair": post["flair"],
                    "created_utc": post["created_utc"]
                }

                conn.execute(posts.insert(), post_db_data)

            logger.info(f"Successfully inserted new rising posts into DB (skipped duplicates)")

    except Exception as e:
        logger.error(f"Failure inserting rising posts data into DB: {e}", exc_info=True)
        raise

def insert_comments(post_comments, post_id):
    """ Inserting comments of Posts into DB in a transaction """
    if not post_comments:
        logger.info("No commments data of Top Posts to insert")
        return

    try:
        with db_session() as conn:
            for comment in post_comments:
                comment_id = comment["id"]

                exists = conn.execute(
                    select(comments.c.id).where(comments.c.id == comment_id)
                ).fetchone()

                # continue iterations if duplicate
                if exists:
                    logger.info(f"The Commment ID: '{comment_id}' already exists. Skipped inserting")
                    continue

                # handling parent_comment_id
                parent_comment_id = comment["parent_id"]
                if parent_comment_id.startswith("t3_"):     # t3_ are top level comments - no parent id
                    parent_comment_id = None
                elif parent_comment_id.startswith("t1_"):   # t1_ are comment replies - parent id
                    parent_comment_id = parent_comment_id[3:]

                comments_db_data = {
                    "id": comment["id"], 
                    "post_id": post_id, 
                    "parent_comment_id": parent_comment_id, 
                    "depth": comment["depth"], 
                    "author": comment["author"],
                    "text": comment["text"],
                    "score": comment["score"],
                    "created_utc": comment["created_utc"],
                }

                conn.execute(comments.insert(), comments_db_data)

            logger.info(f"Successfully inserted comments of Post '{post_id}' into DB (skipped duplicates)")

    except Exception as e:
        logger.error(f"Failure inserting comments of Post '{post_id}' into DB: {e}", exc_info=True)
        raise


def insert_post_sentiment(post_data):
    """ Inserting the Sentiment of posts into DB in a transaction """

    if not post_data:
        logger.info("No post data to insert")
        return

    post_sentiment_to_insert = []

    for post in post_data:
        post_sentiment_db_data = {
            "post_id": post["id"],
            "title_sentiment": post["title_sentiment"],
            "body_sentiment": post["body_sentiment"],
            "score": post["score"],
            "upvote_ratio": post["upvote_ratio"],
            "controversiality": post["controversiality"],
            "num_comments": post["num_comments"],
        }
        post_sentiment_to_insert.append(post_sentiment_db_data)

    try:
        with db_session() as conn:
            conn.execute(post_sentiment_history.insert(), post_sentiment_to_insert)

        logger.info(f"Successfully inserted sentiment of post/s into DB")

    except Exception as e:
        logger.error(f"Failure inserting sentiment of post/s into DB: {e}", exc_info=True)
        raise

def insert_comment_sentiment(post_comments):
    """ Inserting the Sentiment of comments into DB in a transaction """
    if not post_comments:
        logger.info("No post comments to insert")
        return

    comment_sentiment_to_insert = []

    for comment in post_comments:
        comment_sentiment_db_data = {
            "comment_id": comment["id"],
            "comment_sentiment": comment["sentiment"],
            "score": comment["score"],
        }
        comment_sentiment_to_insert.append(comment_sentiment_db_data)

    try:
        with db_session() as conn:
            conn.execute(comment_sentiment_history.insert(), comment_sentiment_to_insert)

        logger.info("Successfully inserted sentiment of comment/s into DB")

    except Exception as e:
        logger.error(f"Failure inserting sentiment of comment/s into DB: {e}", exc_info=True)
        raise


def retrieve_metadata(subreddit_name: str) -> Optional[Dict[str, Any]]:
    """ Read basic subreddit metadata (name, description, subscriber count, created at) from DB by name """
    try:
        with db_session() as conn:
            result = conn.execute(
                select(
                    subreddits.c.description,
                    subreddits.c.subscriber_count,
                    subreddits.c.created_utc
                ).where(subreddits.c.name == subreddit_name)
            ).fetchone()

            if not result:
                logger.warning(f"Subreddit '{subreddit_name}' not found in Database")
                return None

            return {
                "name": subreddit_name,
                "description": result.description,
                "subscribers": result.subscriber_count,
                "created_at": result.created_utc
            }

    except Exception as e:
        logger.error(f"Failed to retrieve metadata for '{subreddit_name}': {e}", exc_info=True)
        raise
