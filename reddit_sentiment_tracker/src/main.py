from reddit_client import fetch_hot_posts, save_to_json

def main():

    # fetching hot posts
    hot_posts = fetch_hot_posts("wien", 5)

    # saving hot posts
    save_to_json(hot_posts, "hot_posts.json")


if __name__ == "__main__":
    main()
