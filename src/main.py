# ~/reddit_sentiment_tracker/reddit_sentiment_tracker/src/main.py

from .data_collection.reddit_client import fetch_top_posts, fetch_rising_posts, save_to_json, get_reddit_client
from config import TOP_POSTS_DATA_PATH, RISING_POSTS_DATA_PATH, RATE_LIMIT_RISING_POSTS, RATE_LIMIT_TOP_POSTS, COMMENT_LIMIT, TOP_POSTS_TIME_FILTER, REPLY_DEPTH
from .data_collection.comment_fetcher import fetch_comments


def main():
    reddit = get_reddit_client()

    top_posts_data = fetch_top_posts("wien",
                                     reddit,
                                     RATE_LIMIT_TOP_POSTS,
                                     TOP_POSTS_TIME_FILTER)

    for post in top_posts_data:
        post_id = post["id"]
        post["comments"] = fetch_comments(reddit,
                                          post_id,
                                          REPLY_DEPTH,
                                          COMMENT_LIMIT)

    rising_posts_data = fetch_rising_posts("wien",
                                           reddit,
                                           RATE_LIMIT_RISING_POSTS)

    for post in rising_posts_data:
        post["comments"] = fetch_comments(reddit,
                                          post["id"],
                                          REPLY_DEPTH,
                                          COMMENT_LIMIT)

# SAVING
    # posts
    save_to_json(top_posts_data,
                 TOP_POSTS_DATA_PATH)
    save_to_json(rising_posts_data,
                 RISING_POSTS_DATA_PATH)

if __name__ == "__main__":
    main()
