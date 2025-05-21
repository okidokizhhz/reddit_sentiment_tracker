# ~/reddit_sentiment_tracker/reddit_sentiment_tracker/src/reddit_client.py
import praw.exceptions
import os
import json
import praw
from dotenv import load_dotenv
from utils import to_vienna_time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# loading environmental variables load_dotenv()
load_dotenv()

# Initialize sentiment analyzer once
sentiment_analyzer = SentimentIntensityAnalyzer()

def get_reddit_client():
    """ Initialize and return authenticated Reddit client using credentials from environment variables. """
    return praw.Reddit(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("SECRET_KEY"),
        user_agent=os.getenv("USER_AGENT"),
        username=os.getenv("REDDIT_USERNAME"),     # Needed for scripts using password grant
        password=os.getenv("REDDIT_PW")
    )

def analyze_sentiment(text):
    """ Analyze text sentiment using VADER """
    return sentiment_analyzer.polarity_scores(text)

def process_post(post):
    """ Process raw post data with sentiment analysis """
    return {
        "id": post.id,
        "title": post.title,
        "title_sentiment": analyze_sentiment(post.title),
        "selftext": post.selftext,
        "body_sentiment": analyze_sentiment(post.selftext),
        "author": str(post.author) if post.author else "N/A",
        "score": post.score,
        "upvote_ratio": post.upvote_ratio,
        "controversiality": (1 - post.upvote_ratio) * post.num_comments,
        "created_utc": to_vienna_time(post.created_utc),
        "num_comments": post.num_comments,
        "url": post.url,
        "awards": len(post.all_awardings),
        "edited": post.edited,
        "flair": post.link_flair_text if post.link_flair_text else None
    }

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


# WRITING / SAVING
def save_to_json(data, file_path):
    """ Saves data to a JSON file. """
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Data saved to {file_path}")
    except Exception as e:
        print(f"Error writing to file: {e}")
