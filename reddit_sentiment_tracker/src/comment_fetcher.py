# ~/reddit_sentiment_tracker/reddit_sentiment_tracker/src/comment_fetcher.py
from reddit_client import analyze_sentiment
from utils import to_vienna_time


def fetch_comments(reddit, post_id: str, REPLY_DEPTH, COMMENT_LIMIT) -> list[dict]:
    """ Basic comment fetcher - gets top-level comments only
    Returns: List of comment dicts with basic info + sentiment """
    limit = COMMENT_LIMIT
    try:
        # returns submission object that contains all the posts data (title, content, author etc)
        submission = reddit.submission(id=post_id)
        # limit=0  -replace placeholder "load more comments" with actual comments - load all comments
        # limit=2  -open 2 placeholder "load more comments" 2 times
        submission.comments.replace_more(limit=REPLY_DEPTH)
        
        comments_data = []

        # using a python slicer ":limit" to limit the amount of comments fetched
        for comment in submission.comments[:limit]:
            comments_data.append({
                "id": comment.id,
                "text": comment.body,
                "author": str(comment.author) if comment.author else "[deleted]",
                "score": comment.score,
                "sentiment": analyze_sentiment(comment.body),  # Your existing function
                "created": to_vienna_time(comment.created_utc)  # Your existing function
            })
        
        return comments_data
    
    except Exception as e:
        print(f"Failed to fetch comments: {e}")
        return []
