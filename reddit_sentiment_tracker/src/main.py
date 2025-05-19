# ~/reddit_sentiment_tracker/reddit_sentiment_tracker/src/main.py

from reddit_client import fetch_data, save_to_json

def main():

    # fetching hot posts
    hot_posts = fetch_data("wien", 5)

    # saving hot posts
    save_to_json(hot_posts)


if __name__ == "__main__":
    main()
