# ~/reddit_sentiment_tracker/src/main.py

from alembic import command
from alembic.config import Config
import os
import asyncio
from .config import RATE_LIMIT_RISING_POSTS, RATE_LIMIT_TOP_POSTS, COMMENT_LIMIT, TOP_POSTS_TIME_FILTER, REPLY_DEPTH
from .data_pipeline_orchestrator import (init_db, reddit_client, get_subreddit_metadata,
                                         subreddit_data_into_db, get_top_posts, top_posts_data_into_db,
                                         comments_top_posts_into_db, get_rising_posts, rising_posts_data_into_db,
                                         comments_rising_posts_into_db)
from .logger import setup_logger

logger = setup_logger("reddit_sentiment_tracker")

def run_migrations():
    """
    Run Alembic migrations using alembic.ini.
    Safe to call once on app startup.
    """
    alembic_cfg = Config(os.path.join(os.path.dirname(__file__), "../alembic.ini"))
    command.upgrade(alembic_cfg, "head")


async def main() -> None:
    run_migrations()
    # Subreddit Name
    subreddit_name = "wien"

    # Initializing DB
    await init_db()

    # Getting Reddit Client
    reddit = await reddit_client()

    try:
        # Fetching Subreddit Metadata
        subreddit_metadata, subreddit_id = await get_subreddit_metadata(subreddit_name, reddit)
        # DB: inserting Metadata
        await subreddit_data_into_db(subreddit_name, subreddit_metadata)

        # Top Posts fetching
        top_posts_data = await get_top_posts(
            subreddit_name,
            reddit,
            RATE_LIMIT_TOP_POSTS,
            TOP_POSTS_TIME_FILTER
        )
        # Inserting Top Posts into DB (with Sentiment)
        await top_posts_data_into_db(top_posts_data, subreddit_id)
        # Commments (top posts) fetching + Inserting into DB
        await comments_top_posts_into_db(
            top_posts_data,
            reddit,
            REPLY_DEPTH,
            COMMENT_LIMIT
        )


        # Rising Posts fetching
        rising_posts_data = await get_rising_posts(
            subreddit_name,
            reddit,
            RATE_LIMIT_RISING_POSTS
        )
        # Inserting Rising Posts into DB (with Sentiment)
        await rising_posts_data_into_db(rising_posts_data, subreddit_id)
        # Rising Posts Comments fetching + Inserting into Db (with Sentiment)
        await comments_rising_posts_into_db(
            rising_posts_data,
            reddit,
            REPLY_DEPTH,
            COMMENT_LIMIT
        )
    except (ValueError, Exception) as e:
        logger.error(f"Data pipeline failed for subreddit '{subreddit_name}': {e}", exc_info=True)
        return

if __name__ == "__main__":
    asyncio.run(main())
