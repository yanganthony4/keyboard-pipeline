import os

from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

APIFY_TOKEN = os.getenv("APIFY_TOKEN")
TASK_ID = os.getenv("TASK_ID")

client = ApifyClient(APIFY_TOKEN)

def get_author_comments(item: list) -> list:
    author_comments = []
    for comment in item:
        if comment.get("isSubmitter") == True:
            author_comments.append(comment)
    return author_comments

def normalize_post(item: dict) -> dict:
    return{
        "source": "reddit",
        "source_post_id": item.get("id"),
        "title": item.get("title"),
        "body": item.get("selftext"),
        "author": item.get("author"),
        "created_utc": item.get("created"),
        "post_url": item.get("url"),
        "gallery_images": item.get("gallery_images", []),
        "author_comments": get_author_comments(item.get("topComments"))
    }

def fetch_posts_hour() -> list[dict]:
    run = client.task(TASK_ID).call()

    dataset_id = run.default_dataset_id

    result = client.dataset(dataset_id).list_items()

    raw_posts = []

    for item in result.items:
        raw_posts.append(normalize_post(item))

    return raw_posts


