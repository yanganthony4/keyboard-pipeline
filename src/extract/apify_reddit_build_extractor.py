import os
import re

from apify_client import ApifyClient
from dotenv import load_dotenv

from src.database.repo.reddit_posts_repo import save_mk_reddit_posts
from html import unescape

load_dotenv()

APIFY_TOKEN = os.getenv("APIFY_TOKEN")
TASK_ID = os.getenv("TASK_ID")

client = ApifyClient(APIFY_TOKEN)

def get_author_comments(item: list) -> list:
    author_comments = []
    for comment in item:
        if comment.get("isSubmitter") == True:
            author_comments.append(comment.get("body"))
    return author_comments

def clean_reddit_text(text):
    if not text:
        return None
    
    text = unescape(text)

    # Normalize Windows / old-style line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove spaces/tabs at the end of each line
    text = re.sub(r"[ \t]+\n", "\n", text)

    # Collapse 3+ blank lines into 2
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove whitespace from start/end of whole post
    return text.strip()

def normalize_post(item: dict) -> dict:
    return{
        "subreddit": "r/MechanicalKeyboards",
        "source_post_id": item.get("id").strip(),
        "title": clean_reddit_text(item.get("title")),
        "body": clean_reddit_text(item.get("selftext")),
        "author": item.get("author"),
        "created_at": item.get("created"),
        "post_url": item.get("url"),
        "gallery_images": item.get("gallery_images", []),
        "author_comments": get_author_comments(item.get("topComments") or [])
    }

def fetch_posts(max_results, time_filter) -> list[dict]:
    run = client.task(TASK_ID).call(
        task_input = {
            "timeFilter": time_filter,
            "maxResults": max_results
        }
    )

    dataset_id = run.default_dataset_id

    result = client.dataset(dataset_id).list_items()

    raw_posts = []

    for item in result.items:
        raw_posts.append(normalize_post(item))

    print(f"Posts Count: {len(raw_posts)}")

    save_mk_reddit_posts(raw_posts)

    return raw_posts




