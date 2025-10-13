# ~/reddit_sentiment_tracker/src/data_collection/post_fetcher.py

import praw.exceptions
from .post_processor import process_post
import logging

logger = logging.getLogger("reddit_sentiment_tracker")

# TOP POSTS
def fetch_top_posts(subreddit_name, reddit, RATE_LIMIT_TOP_POSTS, TOP_POSTS_TIME_FILTER):
    """ Fetches top posts from a subreddit """
    try:
        # accessing subreddit
        subreddit = reddit.subreddit(subreddit_name)
    except Exception as e:
        print(f"Error accessing subreddit: {e}")

    top_posts_data = []

    # fetching data of subreddit
    try:
        for post in subreddit.top(limit=RATE_LIMIT_TOP_POSTS,
                                  time_filter=TOP_POSTS_TIME_FILTER):
            top_posts_data.append(process_post(post))

        return top_posts_data 

    except praw.exceptions.APIException as e:
        print(f"Reddit API Exception: {e}")
        return []
    except Exception as e:
        print(f"Error fetching '{subreddit_name}' data: {e}")
        return []

# RISING POSTS
def fetch_rising_posts(subreddit_name, reddit, RATE_LIMIT_RISING_POSTS):
    """ Fetches rising posts from a subreddit. """
    try:
        # accessing subreddit
        subreddit = reddit.subreddit(subreddit_name)
    except Exception as e:
        print(f"Error accessing subreddit: {e}")

    rising_posts_data = []

    # fetching data of subreddit
    try:
        for post in subreddit.rising(limit=RATE_LIMIT_RISING_POSTS):
            rising_posts_data.append(process_post(post))

        return rising_posts_data 

    except praw.exceptions.APIException as e:
        print(f"Reddit API Exception: {e}")
        return []
    except Exception as e:
        print(f"Error fetching '{subreddit_name}' data: {e}")
        return []
