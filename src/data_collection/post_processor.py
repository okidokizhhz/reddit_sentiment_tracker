# ~/reddit_sentiment_tracker/src/data_collection/post_processor.py

from ..utils.utils import to_vienna_time
from ..sentiment_analysis.sentiment_analyzer import analyze_sentiment
import logging

logger = logging.getLogger("reddit_sentiment_tracker")

def process_post(post):
    """ Process raw post data with sentiment analysis """
    return {
        "id": post.id,
        "author": str(post.author) if post.author else "N/A",
        "created_utc": to_vienna_time(post.created_utc),
        "num_comments": post.num_comments,
        "url": post.url,
        "awards": len(post.all_awardings),
        "edited": post.edited,
        "flair": post.link_flair_text if post.link_flair_text else None,
        "title": post.title,
        "title_sentiment": analyze_sentiment(post.title),
        "selftext": post.selftext,
        "body_sentiment": analyze_sentiment(post.selftext),
        "score": post.score,
        "upvote_ratio": post.upvote_ratio,
        "controversiality": (1 - post.upvote_ratio) * post.num_comments
    }
