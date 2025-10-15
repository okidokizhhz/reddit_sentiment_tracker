# ~/reddit_sentiment_tracker/src/data_collection/subreddit_fetcher.py

import praw
import praw.exceptions
import logging

logger = logging.getLogger("reddit_sentiment_tracker")

def fetch_subreddit_metadata(subreddit_name: str, reddit) -> dict:
    """ Fetches metadata of a specific subreddit """
    try:
        subreddit = reddit.subreddit(subreddit_name)

        # fetching metadata
        metadata = {
            "id": subreddit.id,
            "name": subreddit.name,
            "description": subreddit.description,
            "subscriber_count": subreddit.subscribers,
            "created_utc": subreddit.created_utc
        }

        logger.info(f"Subreddit Metadata of: '{subreddit_name}' successfully fetched")

        return metadata

    except praw.exceptions.APIException as e:
        logger.error(f"Reddit API Exception while fetching metadata of subreddit '{subreddit_name}': {e}")
        return {}
    except Exception as e:
        logger.error(f"Error fetching metadata of subreddit '{subreddit_name}': {e}", exc_info=True)
        return {}
