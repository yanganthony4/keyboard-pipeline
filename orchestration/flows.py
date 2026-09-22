from pathlib import Path
import subprocess
import sys

from prefect import flow, task

REPO_ROOT = Path(__file__).resolve().parents[1]

DBT_PROJECT_DIR = (
    Path(__file__).resolve().parents[1]
    / "analytics"
    / "keyboard_dbt"
)

@task
def scrape_reddit():
    subprocess.run(
        [
            sys.executable,
            "-m",
            "src.web_scraper.apify_reddit_build_extractor",
        ],
        cwd=REPO_ROOT,
        check=True,
    )

@task
def build_dbt():
    subprocess.run(
        [
            "dbt",
            "build",
            "--profiles-dir",
            ".",
        ],
        cwd=DBT_PROJECT_DIR,
        check=True,
    )


@flow(name="keyboard-dbt-build")
def keyboard_dbt_flow():
    scrape_reddit()
    build_dbt()


if __name__ == "__main__":
    keyboard_dbt_flow()