import os
import re

from apify_client import ApifyClient
from dotenv import load_dotenv
from html import unescape

from src.database.repo.reddit_posts_repo import save_mk_reddit_posts


load_dotenv()

APIFY_TOKEN = os.getenv("APIFY_TOKEN")
TASK_ID = os.getenv("APIFY_TASK_ID")

client = ApifyClient(APIFY_TOKEN)


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


def get_gallery_images(item: dict) -> list:
    gallery_images = []

    for image in item.get("gallery_images") or []:
        image_url = image.get("url")

        if image_url:
            gallery_images.append(image_url)

    return gallery_images


def get_author_comments(
    post_id: str,
    comments: list[dict]
) -> list:

    author_comments = []

    for comment in comments:
        if (
            comment.get("postId") == post_id
            and comment.get("is_submitter") is True
        ):
            body = clean_reddit_text(
                comment.get("body")
            )

            if body:
                author_comments.append(body)

    return author_comments


def normalize_post(
    item: dict,
    comments: list[dict]
) -> dict:

    post_id = item.get("id")

    return {
        "subreddit": item.get(
            "subreddit_name_prefixed",
            "r/MechanicalKeyboards"
        ),

        "source_post_id": post_id,

        "title": clean_reddit_text(
            item.get("title")
        ),

        "body": clean_reddit_text(
            item.get("body")
        ),

        "author": item.get("author"),

        "created_at": item.get(
            "created_utc"
        ),

        "post_url": (
            item.get("canonical_url")
            or item.get("url")
        ),

        "gallery_images": get_gallery_images(
            item
        ),

        "author_comments": get_author_comments(
            post_id,
            comments
        )
    }


def process_run(run) -> list[dict]:
    dataset_id = run.default_dataset_id

    result = client.dataset(
        dataset_id
    ).list_items()

    posts = []
    comments = []

    # Actor returns posts and comments as separate records
    for item in result.items:
        if item.get("kind") == "post":
            posts.append(item)

        elif item.get("kind") == "comment":
            comments.append(item)

    print(f"Posts Found: {len(posts)}")
    print(f"Comments Found: {len(comments)}")

    normalized_posts = []

    for post in posts:
        normalized_post = normalize_post(
            post,
            comments
        )

        normalized_posts.append(
            normalized_post
        )

    print(
        f"Posts Normalized: "
        f"{len(normalized_posts)}"
    )

    save_mk_reddit_posts(
        normalized_posts
    )

    return normalized_posts


def fetch_posts_by_date(
    max_results,
    date_from,
    date_to
) -> list[dict]:

    print(
        f"Fetching Reddit posts from "
        f"{date_from} to {date_to}..."
    )

    run = client.task(
        TASK_ID
    ).call(
        task_input={
            "maxPosts": max_results,
            "dateFrom": date_from,
            "dateTo": date_to,
            "subredditTimeframe": "all"
        }
    )

    return process_run(run)


def fetch_recent_posts(
    max_results=100
) -> list[dict]:

    print(
        "Fetching Reddit posts "
        "from the last 24 hours..."
    )

    run = client.task(
        TASK_ID
    ).call(
        task_input={
            "maxPosts": max_results,
            "subredditTimeframe": "day"
        }
    )

    return process_run(run)


if __name__ == "__main__":

    # Normal daily pipeline
    # fetch_recent_posts(
    #     max_results=100
    # )

    # Historical/backfill example:
    #
    fetch_posts_by_date(
        max_results=5,
        date_from="2026-09-01",
        date_to="2026-09-02"
    )