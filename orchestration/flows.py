from pathlib import Path
import subprocess
import json

from prefect import flow, task
from src.web_scraper.apify_reddit_build_extractor import fetch_posts_by_date, fetch_recent_posts_day

REPO_ROOT = Path(__file__).resolve().parents[1]

DBT_PROJECT_DIR = (
    Path(__file__).resolve().parents[1]
    / "analytics"
    / "keyboard_dbt"
)

@task
def scrape_reddit_daily(max_posts: int):
    scrape_run_id = fetch_recent_posts_day(max_posts)

    return scrape_run_id

@task
def scrape_reddit_by_date(max_posts: int, date_from, date_to):
    scrape_run_id = fetch_posts_by_date(max_posts, date_from, date_to)

    return scrape_run_id
    
@task
def build_reddit_models(scrape_run_id: int):
    dbt_vars = json.dumps({
        "scrape_run_id": scrape_run_id
    })

    subprocess.run(
        [
            "dbt",
            "build",

            "--select",
            "reddit_search_documents+",

            "--vars",
            dbt_vars,

            "--profiles-dir",
            ".",
        ],
        cwd=DBT_PROJECT_DIR,
        check=True,
    )


@flow(name="keyboard-reddit-daily")
def keyboard_reddit_daily(
    max_posts: int = 100
):
    scrape_run_id = scrape_reddit_daily(max_posts)

    if scrape_run_id is None:
        raise RuntimeError("Reddit scrape did not return a scrape_run_id")

    build_reddit_models(scrape_run_id)


@flow(name="keyboard-reddit-date-range")
def keyboard_reddit_date_range(
    max_posts: int,
    date_from: str,
    date_to: str,
):
    scrape_run_id = scrape_reddit_by_date(
        max_posts,
        date_from,
        date_to,
    )

    if scrape_run_id is None:
        raise RuntimeError("Reddit scrape did not return a scrape_run_id")

    build_reddit_models(scrape_run_id)


if __name__ == "__main__":
    keyboard_reddit_daily()