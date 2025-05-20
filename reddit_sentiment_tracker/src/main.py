# ~/reddit_sentiment_tracker/reddit_sentiment_tracker/src/main.py

from reddit_client import fetch_top_posts, fetch_rising_posts, save_to_json
from config import TOP_POSTS_DATA_PATH, RISING_POSTS_DATA_PATH

def main():

    # fetching top posts
    top_posts_data = fetch_top_posts("wien")
    # fetching rising posts
    rising_posts_data = fetch_rising_posts("wien")

    # if top_posts_data:
        # for post_data in top_posts_data:
            # get_comments(post_data)
    # # fetching comments from posts
    # comments_data = get_comments(top_posts_data)

    # saving hot posts
    save_to_json(top_posts_data, TOP_POSTS_DATA_PATH)
    save_to_json(rising_posts_data, RISING_POSTS_DATA_PATH)

    # save_to_json(comments_data)


if __name__ == "__main__":
    main()
