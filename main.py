from src.extract.apify_reddit_build_extractor import fetch_posts_hour

def main():
    posts = fetch_posts_hour()

    print(posts)
    print(len(posts))

if __name__ == "__main__":
    main()
    