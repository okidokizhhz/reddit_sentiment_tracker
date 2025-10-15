# ~/reddit_sentiment_tracker/src/main.py

import sys
from .data_collection.reddit_client import get_reddit_client
from .data_collection.post_fetcher import fetch_top_posts, fetch_rising_posts
from .data_collection.comment_fetcher import fetch_comments
from .data_collection.subreddit_fetcher import fetch_subreddit_metadata
from .config import RATE_LIMIT_RISING_POSTS, RATE_LIMIT_TOP_POSTS, COMMENT_LIMIT, TOP_POSTS_TIME_FILTER, REPLY_DEPTH
from .storage.connection import initialize_database
from .storage.crud import insert_subreddit_metadata, insert_top_posts, insert_rising_posts, insert_comments
from .logger import setup_logger

logger = setup_logger("reddit_sentiment_tracker")

def main():
    subreddit_name = "wien"

    # Database Initialization
    try:
        initialize_database()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.critical(f"Failed to initialize DB: {e}. Exiting Program", exc_info=True)
        sys.exit(1)

    # Reddit Client
    try:
        reddit = get_reddit_client()
        logger.info("Reddit Client retrieved successfully")
    except Exception as e:
        logger.fatal(f"Failed to retrieve Reddit client: {e}. Exiting Program", exc_info=True)
        sys.exit(1)         # Exit program on failure


    # Subreddit Metadata fetching
    try:
        subreddit_metadata = fetch_subreddit_metadata(subreddit_name, reddit)
        logger.info(f"Subreddit metadata of 'r/{subreddit_name}' fetched successfully")
        subreddit_id = subreddit_metadata["id"]
    except Exception as e:
        logger.error(f"Failed to fetch metadata of: r/{subreddit_name}", exc_info=True)


    # DB: inserting Metadata
    try:
        insert_subreddit_metadata(subreddit_metadata)
        logger.info(f"Subreddit metadata of 'r/{subreddit_name}' inserted into DB successfully")
    except Exception as e:
        logger.error(f"Failed to insert subreddit metadata of 'r/{subreddit_name}' into DB: {e}", exc_info=True)


    # Top Posts fetching
    try:
        top_posts_data = fetch_top_posts(subreddit_name,
                                         reddit,
                                         RATE_LIMIT_TOP_POSTS,
                                         TOP_POSTS_TIME_FILTER)
    except Exception as e:
        logger.error(f"Failed to fetch top posts", exc_info=True)

    # DB: inserting Top Posts
    try:
        insert_top_posts(top_posts_data, subreddit_id)
        logger.info("Inserting top posts data into DB successful")
    except Exception as e:
        logger.error(f"Failed to insert top posts data into DB: {e}", exc_info=True)

    # Top Posts Comments fetching
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
                logger.info(f"Post id {post_id}: Inserting comments of Top Posts into DB successful")

            except Exception as e:
                logger.error(f"Post id {post_id}: Failed to insert comments of Top Posts into DB: {e}", exc_info=True)
    except Exception as e:
        logger.error(f"Failed to fetch comments for Top Posts", exc_info=True)


    # Rising Posts fetching
    try:
        rising_posts_data = fetch_rising_posts(subreddit_name,
                                               reddit,
                                               RATE_LIMIT_RISING_POSTS)
    except Exception as e:
        logger.error(f"failed to fetch rising posts: {e}", exc_info=True)


    # DB: inserting Rising Posts
    try: 
        insert_rising_posts(rising_posts_data, subreddit_id)
        logger.info("Inserting rising posts data into DB successful")
    except Exception as e:
        logger.error(f"Failed to insert rising posts data into DB: {e}", exc_info=True)


    # Rising Posts Comments fetching
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
                logger.info(f"Post id {post_id}: Inserting comments of Rising Posts into DB successful")

            except Exception as e:
                logger.error(f"Post id {post_id}: Failed to insert comments of Rising Posts into DB: {e}", exc_info=True)


    except Exception as e:
        logger.error(f"Failed to fetch comments for Rising Posts", exc_info=True)


if __name__ == "__main__":
    main()
