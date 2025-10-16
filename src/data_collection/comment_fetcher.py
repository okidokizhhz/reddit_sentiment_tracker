# ~/reddit_sentiment_tracker/src/data_collection/comment_fetcher.py

from ..sentiment_analysis.sentiment_analyzer import analyze_sentiment
from datetime import datetime, timezone
from typing import Any
import logging

logger = logging.getLogger("reddit_sentiment_tracker")

def fetch_comments(reddit, post_id: str, REPLY_DEPTH: int, COMMENT_LIMIT: int) -> list[dict[str, Any]]:
    """ 
    Comment fetcher - gets top-level comments only
    Returns: List of comment dicts with basic info + sentiment
    """
    try:
        # returns submission object that contains all the posts data (title, content, author etc)
        submission = reddit.submission(id=post_id)
        # limit=0  -replace placeholder "load more comments" with actual comments - load all comments
        # limit=2  -open 2 placeholder "load more comments" 2 times
        submission.comments.replace_more(limit=REPLY_DEPTH)
        
        comments_data = []
        limit = COMMENT_LIMIT

        # using a python slicer ":limit" to limit the amount of comments fetched
        for comment in submission.comments[:limit]:
            comments_data.append({
                "id": comment.id,
                "parent_id": comment.parent_id,                     # id of the parent of comment
                "depth": comment.depth,                             # nesting level (0 = top-level)
                "text": comment.body,
                "author": str(comment.author) if comment.author else "[deleted]",
                "score": comment.score,
                "edited": comment.edited,
                "created_utc": datetime.fromtimestamp(comment.created_utc, tz=timezone.utc),
                "sentiment": analyze_sentiment(comment.body)  # Your existing function
            })
        
        logger.info(f"Fetching {len(comments_data)} comments of {post_id} successful")

        return comments_data
    
    except Exception as e:
        logger.error(f"Failed to fetch comments for post {post_id}: {e}", exc_info=True)
        return []
