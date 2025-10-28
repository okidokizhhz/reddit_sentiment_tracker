# ~/reddit_sentiment_tracker/src/data_collection/subreddit_fetcher.py

import praw
import praw.exceptions
from datetime import datetime, timezone
from typing import Any, Optional, Dict
import logging

logger = logging.getLogger("reddit_sentiment_tracker")

def fetch_subreddit_metadata(subreddit_name: str, reddit: Any) -> Optional[Dict[str, Any]]:
    """ Fetches metadata of a specific subreddit """
    try:
        subreddit = reddit.subreddit(subreddit_name)

        # fetching metadata
        metadata = {
            "id": subreddit.id,
            "name": subreddit.display_name,
            "description": subreddit.description,
            "subscriber_count": subreddit.subscribers,
            "created_utc": datetime.fromtimestamp(subreddit.created_utc, tz=timezone.utc)
        }

        logger.info(f"Subreddit Metadata of: '{subreddit_name}' successfully fetched")

        return metadata

    except praw.exceptions.APIException as e:
        logger.error(f"Reddit API Exception while fetching metadata of subreddit '{subreddit_name}': {e}")
        return None
    except Exception as e:
        logger.error(f"Error fetching metadata of subreddit '{subreddit_name}': {e}", exc_info=True)
        return None
