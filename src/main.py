# ~/reddit_sentiment_tracker/src/main.py

from .config import RATE_LIMIT_RISING_POSTS, RATE_LIMIT_TOP_POSTS, COMMENT_LIMIT, TOP_POSTS_TIME_FILTER, REPLY_DEPTH
from .data_pipeline_orchestrator import (init_db, reddit_client, get_subreddit_metadata,
                                         subreddit_data_into_db, get_top_posts, top_posts_data_into_db,
                                         comments_top_posts_into_db, get_rising_posts, rising_posts_data_into_db,
                                         comments_rising_posts_into_db)
from .logger import setup_logger

logger = setup_logger("reddit_sentiment_tracker")

def main() -> None:
    # Subreddit Name
    subreddit_name = "wien"

    # Initializing DB
    init_db()

    # Getting Reddit Client
    reddit = reddit_client()

    try:
        # Fetching Subreddit Metadata
        subreddit_metadata, subreddit_id = get_subreddit_metadata(subreddit_name, reddit)
        # DB: inserting Metadata
        subreddit_data_into_db(subreddit_name, subreddit_metadata)

        # Top Posts fetching
        top_posts_data = get_top_posts(
            subreddit_name,
            reddit,
            RATE_LIMIT_TOP_POSTS,
            TOP_POSTS_TIME_FILTER
        )
        # Inserting Top Posts into DB (with Sentiment)
        top_posts_data_into_db(top_posts_data, subreddit_id)
        # Commments (top posts) fetching + Inserting into DB
        comments_top_posts_into_db(
            top_posts_data,
            reddit,
            REPLY_DEPTH,
            COMMENT_LIMIT
        )


        # Rising Posts fetching
        rising_posts_data = get_rising_posts(
            subreddit_name,
            reddit,
            RATE_LIMIT_RISING_POSTS
        )
        # Inserting Rising Posts into DB (with Sentiment)
        rising_posts_data_into_db(rising_posts_data, subreddit_id)
        # Rising Posts Comments fetching + Inserting into Db (with Sentiment)
        comments_rising_posts_into_db(
            rising_posts_data,
            reddit,
            REPLY_DEPTH,
            COMMENT_LIMIT
        )
    except (ValueError, Exception) as e:
        logger.error(f"Data pipeline failed for subreddit '{subreddit_name}': {e}", exc_info=True)
        return

if __name__ == "__main__":
    main()
