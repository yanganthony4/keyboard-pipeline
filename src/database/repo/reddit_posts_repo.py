from src.database.raw import (
    create_scrape_run,
    complete_scrape_run,
    fail_scrape_run,
)

from src.database.connection import get_connection

from psycopg.types.json import Jsonb

def create_reddit_posts_record(
        conn,
        scrape_run_id,
        post_url,
        subreddit,
        source_post_id,
        title,
        body,
        author,
        created_at,
        gallery_images,
        author_comments,
):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO raw.reddit_posts (
                scrape_run_id,
                post_url,
                subreddit,
                source_post_id,
                title,
                body,
                author,
                created_at,
                gallery_images,
                author_comments
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            ON CONFLICT (scrape_run_id, source_post_id)
            DO NOTHING;
            """,
            (
                scrape_run_id,
                post_url,
                subreddit,
                source_post_id,
                title,
                body,
                author,
                created_at,
                Jsonb(gallery_images),
                Jsonb(author_comments)
            ),
        )

def save_mk_reddit_posts(reddit_posts):
    with get_connection() as conn:
        scrape_run_id = create_scrape_run(conn, "reddit")

        print(f"Storing scrape {scrape_run_id}: reddit")

        # Preserve evidence that this scrape run occurred.
        conn.commit()

        try:
            for post in reddit_posts:
                create_reddit_posts_record(
                    conn = conn,
                    scrape_run_id = scrape_run_id,
                    post_url = post.get("post_url"),
                    subreddit = post.get("subreddit"),
                    source_post_id = post.get("source_post_id"),
                    title = post.get("title"),
                    body = post.get("body"),
                    author = post.get("author"),
                    created_at = post.get("created_at"),
                    gallery_images = post.get("gallery_images", []),
                    author_comments = post.get("author_comments", []),
                )
            
            complete_scrape_run(
                conn,
                scrape_run_id,
                len(reddit_posts)
            )

            conn.commit()

            return True
    
        except Exception as error:
            conn.rollback()

            print(f"ERROR: {error}")

            fail_scrape_run(
                conn,
                scrape_run_id,
                str(error),
            )

            conn.commit()

            raise
    