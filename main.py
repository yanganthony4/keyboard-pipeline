from src.extract.apify_reddit_build_extractor import fetch_posts

def main():
    posts = fetch_posts(2, "day")

    print(posts)
    print(len(posts))

if __name__ == "__main__":
    main()
    