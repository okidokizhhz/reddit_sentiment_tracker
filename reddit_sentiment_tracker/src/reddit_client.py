# REDDIT SENTIMENT TRACKER
# ~/reddit_sentiment_tracker/reddit_sentiment_tracker/src/reddit_client.py

import praw.exceptions
import os
import json
import praw
from dotenv import load_dotenv
from config import FETCHED_DATA_PATH
from utils import to_vienna_time

# loading environmental variables
load_dotenv()

def get_reddit_client():
    """ 
    Initializes and returns a Reddit client using credentials from environment variables
    """

    return praw.Reddit(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("SECRET_KEY"),
        user_agent=os.getenv("USER_AGENT"),
        username=os.getenv("REDDIT_USERNAME"),     # Needed for scripts using password grant
        password=os.getenv("REDDIT_PW")
    )


def fetch_data(subreddit_name, RATE_LIMIT):
    """
    Fetches hot posts from a given subreddit.
    """


    # initialize reddit client
    reddit = get_reddit_client()
    # access a subreddit
    subreddit = reddit.subreddit(subreddit_name)

    hot_posts = []

    try:
        # Fetch posts with Rate Limits
        for post in subreddit.hot(limit=RATE_LIMIT):
            hot_posts.append({
                "id": post.id,
                "title": post.title,
                "selftext": post.selftext,
                "author": str(post.author) if post.author else "N/A",  # Handles deleted users
                "score": post.score,
                "upvote-ratio": post.upvote_ratio,
                "created-utc": to_vienna_time(post.created_utc),  # Unix timestamp
                "num-comments": post.num_comments,
                "url": post.url,
                "awards": len(post.all_awardings), # Indicator for community appreciation
                "edited": post.edited # bool or timestamp if edited
            })

        # returning the list with the fetched data
        return hot_posts

    except praw.exceptions.APIException as e:
        print(f"Reddit API Exception: {e}")
    except Exception as e:
        print(f"Error: {e}")


# write posts list to JSON
def save_to_json(data):
    """
    Saves data to a JSON file.
    """

    try:
        with open(FETCHED_DATA_PATH, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Data saved to {FETCHED_DATA_PATH}")
    except Exception as e:
        print(f"Error writing to file: {e}")
