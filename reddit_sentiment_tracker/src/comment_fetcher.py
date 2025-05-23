# ~/reddit_sentiment_tracker/reddit_sentiment_tracker/src/comment_fetcher.py
from reddit_client import analyze_sentiment
from utils import to_vienna_time

def fetch_comments(reddit, post_id, REPLY_DEPTH, COMMENT_LIMIT) -> list[dict]:
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
                "created": to_vienna_time(comment.created_utc),  # Your existing function
                "sentiment": analyze_sentiment(comment.body)  # Your existing function
            })
        
        return comments_data
    
    except Exception as e:
        print(f"Failed to fetch comments: {e}")
        return []
