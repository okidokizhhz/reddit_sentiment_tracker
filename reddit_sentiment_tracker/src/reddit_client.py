# REDDIT SENTIMENT TRACKER
import json
import praw
from dotenv import load_dotenv
import praw.exceptions
import os

# loading environmental variables
load_dotenv()

def get_reddit_client():
    """ Initializes and returns a Reddit client using credentials from environment variables

    Returns
    -------
    praw.Reddit
        Authenticated Reddit client object
    """

    return praw.Reddit(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("SECRET_KEY"),
        user_agent=os.getenv("USER_AGENT"),
        username=os.getenv("REDDIT_USERNAME"),     # Needed for scripts using password grant
        password=os.getenv("REDDIT_PW")
    )


def fetch_hot_posts(subreddit_name, RATE_LIMIT):
    """
    Fetches hot posts from a given subreddit.

    Parameters
    ----------
    subreddit_name : str
        Name of the subreddit to fetch posts from.
    RATE_LIMIT : int
        Maximum number of posts to retrieve.

    Returns
    -------
    list of dict
        A list containing dictionaries of post metadata (title, score, etc.).
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
                "Title": post.title,
                "Score": post.score,
                "ID": post.id,
                "URL": post.url,
                "Created": post.created_utc,  # Unix timestamp
                "Author": str(post.author) if post.author else "N/A",  # Handles deleted users
                "Number of Comments": post.num_comments
            })

        # returning the list with the fetched data
        return hot_posts

    except praw.exceptions.APIException as e:
        print(f"Reddit API Exception: {e}")
    except Exception as e:
        print(f"Error: {e}")


# write posts list to JSON
def save_to_json(data, filepath):
    """
    Saves data to a JSON file.

    Parameters
    ----------
    data : any serializable object
        The data to save to file.
    filepath : str
        Path to the output JSON file.
    """

    try:
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Data saved to {filepath}")
    except Exception as e:
        print(f"Error writing to file: {e}")
