# REDDIT SENTIMENT TRACKER
# ~/reddit_sentiment_tracker/reddit_sentiment_tracker/src/reddit_client.py

import praw.exceptions
import os
import json
import praw
from dotenv import load_dotenv
from config import RATE_LIMIT_TOP_POSTS, RATE_LIMIT_RISING_POSTS
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


# TOP POSTS
def fetch_top_posts(subreddit_name):
    """
    Fetches top posts from a subreddit.
    """

    # initialize reddit client
    reddit = get_reddit_client()
    # access a subreddit
    subreddit = reddit.subreddit(subreddit_name)

    top_posts_data = []

    try:
        # Fetch posts with Rate Limits
        for post in subreddit.top(limit=RATE_LIMIT_TOP_POSTS):

            top_posts_data.append({
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
        return top_posts_data 

    except praw.exceptions.APIException as e:
        print(f"Reddit API Exception: {e}")
    except Exception as e:
        print(f"Error: {e}")

# RISING POSTS
def fetch_rising_posts(subreddit_name):
    """
    Fetches rising posts from a subreddit.
    """

    # initialize reddit client
    reddit = get_reddit_client()
    # access a subreddit
    subreddit = reddit.subreddit(subreddit_name)

    rising_posts_data = []

    try:
        # Fetch posts with Rate Limits
        for post in subreddit.rising(limit=RATE_LIMIT_RISING_POSTS):

            rising_posts_data.append({
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
        return rising_posts_data 

    except praw.exceptions.APIException as e:
        print(f"Reddit API Exception: {e}")
    except Exception as e:
        print(f"Error: {e}")

# COMMENTS
# def get_comments(post):
    # """
    # Gets basic comment data from a Reddit post
    # - Only fetches top-level comments
    # - No sorting by score
    # - Just gets first few comments
    # """
    
    # comments_data = []
    
    # # Make sure we have all comments loaded
    # post.comments.replace_more(limit=0)
    
    # # Count how many comments we've processed
    # comment_count = 0
    
    # for comment in post.comments:
        # # Only process top-level comments (direct replies to post)
        # if comment.is_root:
            # comments_data.append({
                # "author": str(comment.author),
                # "text": comment.body,
                # "upvotes": comment.score,
                # "created": to_vienna_time(comment.created_utc)
            # })
            
            # comment_count += 1
            # if comment_count >= COMMENT_LIMIT:
                # break
    
    # return comments_data


# write posts list to JSON
def save_to_json(data, file_path):
    """
    Saves data to a JSON file.
    """

    try:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Data saved to {file_path}")
    except Exception as e:
        print(f"Error writing to file: {e}")
