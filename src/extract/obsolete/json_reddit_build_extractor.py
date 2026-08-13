import requests

BASE_URL = "https://www.reddit.com"
SUBREDDIT = "MechanicalKeyboards"
SEARCH_URL = f"{BASE_URL}/r/{SUBREDDIT}/search.rss"

HEADERS = {
    "User-Agent": "keyboard-pipeline/0.1"
}

# Get a list of image urls if available
def reddit_get_image_urls(post_data: dict) ->  list[str]:

    image_urls = []

    # Gallery post containing multiple images
    if post_data.get("is_gallery"):
        gallery_data = post_data.get("gallery_data", {})
        media_metadata = post_data.get("media_metadata", {})

        for item in gallery_data.get("items", []):
            media_id = item.get("media_id")

            if media_id in media_metadata:
                media = media_metadata[media_id]

                source = media.get("s", {})
                image_url = source.get("u")

                if image_url:
                    image_urls.append(image_url)
        return image_urls

    # Regular Single-Image post
    if post_data.get("post_hint") == "image":
        image_url = post_data.get("url")

        if image_url:
            image_urls.append(image_url)

        return image_urls
    
    # Reddit Preview
    preview = post_data.get("preview")
    
    if preview:
        images = preview.get("images", [])
        
        for image in images:
            source = image.get("source", {})
            image_url = source.get("url")

            if image_url:
                image_urls.append(image_url)
    return image_urls
    
# Fetch author comments
def reddit_get_author_comments(
        post_permalink: str,
        post_author: str
) -> list[dict]:
    url = f"{BASE_URL}{post_permalink}.json"

    response = requests.get(
        url,
        headers = HEADERS,
        timeout = 10
    )

    # Raise an exception (404, 403 Forbidden, 500 Server Error)
    print("Status:", response.status_code)
    print("Response:")
    print(response.text[:1000])

    response.raise_for_status()

    data = response.json()

    comment_items = data[1]["data"]["children"]

    author_comments = []

    def reddit_search_comments(items: list[dict]) -> None:
        for item in items:
            # t1 = comment
            if item.get("kind") != "t1":
                continue

            # Get comment data
            comment = item["data"]

            if comment.get("author") == post_author:
                author_comments.append({
                    "comment_id": comment.get("id"),
                    "comment_fullname": comment.get("name"),
                    "author": comment.get("author"),
                    "author_fullname": comment.get("author_fullname"),
                    "body": comment.get("body"),
                    "created_utc": comment.get("created_utc"),
                    "score": comment.get("score"),
                    "parent_id": comment.get("parent_id"),
                    "link_id": comment.get("link_id"),
                    "permalink": comment.get("permalink")
                })

            # Search through nested replies
            replies = comment.get("replies")

            if isinstance(replies, dict):
                reply_items = replies["data"]["children"]

                reddit_search_comments(reply_items)
    
    reddit_search_comments(comment_items)

    return author_comments

    # more logic
    
# Fetch posts and put into 
def fetch_reddit_posts(limit: int = 10) -> list[dict]:

    params = {
    "q": 'flair:"Builds"',
    "restrict_sr": 1,
    "sort": "new",
    "limit": limit
    }


    response = requests.get(
        SEARCH_URL,
        headers = HEADERS,
        params = params,
        timeout = 10
    )

    print("Status:", response.status_code)
    print("Response:")
    print(response.text[:1000])

    response.raise_for_status()

    data = response.json()

    posts = []

    for item in data["data"]["children"]:

        post = item["data"]

        post_id = post.get("id")
        author = post.get("author")
        permalink = post.get("permalink")

        raw_post = {
            # Common source identity
            "source": "reddit",
            "source_post_id": post_id,
            "source_author_id": post.get("author_fullname"),

            # Core content
            "title": post.get("title"),
            "body": post.get("selftext"),
            "author": author,
            "created_utc": post.get("created_utc"),

            "post_url": (
                BASE_URL + permalink
                if permalink
                else None
            ),

            "image_urls": reddit_get_image_urls(post),

            # Discussion/content related
            "author_comments": (
                reddit_get_author_comments(permalink, author)
                if permalink and author
                else []
            ),

            # Source-specific metadata
            "source_metadata": {
                "score": post.get("score"),
                "upvote_ratio": post.get("upvote_ratio"),
                "num_comments": post.get("num_comments"),
                "subreddit": post.get("subreddit"),
                "flair": post.get("link_flair_text"),
                "post_fullname": post.get("name")
            }
        }

        posts.append(raw_post)

    return posts
