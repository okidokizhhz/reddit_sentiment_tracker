# ~/reddit_sentiment_tracker/src/data_collection/reddit_client.py

import os
import praw
from dotenv import load_dotenv
import logging

logger = logging.getLogger("reddit_sentiment_tracker")

# loading environmental variables load_dotenv()
load_dotenv()

def get_reddit_client() -> praw.Reddit:
    """ Initialize and return authenticated Reddit client using credentials from environment variables. """
    try:
        client = praw.Reddit(
            client_id=os.getenv("CLIENT_ID"),
            client_secret=os.getenv("SECRET_KEY"),
            user_agent=os.getenv("USER_AGENT"),
            username=os.getenv("REDDIT_USERNAME"),     # Needed for scripts using password grant
            password=os.getenv("REDDIT_PW")
        )
        logger.info("Reddit Client retrieval success")
        return client

    except Exception as e:
        logger.error(f"Error retrieving Reddit Client: {e}", exc_info=True)
        raise
