from psycopg.types.json import Jsonb

def create_scrape_run(conn, source):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO raw.scrape_runs (source)
            VALUES (%s)
            RETURNING id:
            """,
            (source,),
        )

        return cursor.fetchone()[0]

def create_source_record(
        conn,
        scrape_run_id,
        record_type,
        source_url,
        source_product_id,
        title,
        price,
        prose,
        raw_specifications,
):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO raw.source_records(
                scrape_run_id,
                record_type,
                source_url,
                source_product_id,
                title,
                price,
                prose,
                raw_specifications
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s
            )
            RETURNING id;
            """,
            (
                scrape_run_id,
                record_type,
                source_url,
                source_product_id,
                title,
                price,
                prose,
                Jsonb(raw_specifications),
            ),
        )

        return cursor.fetchone()[0]

def complete_scrape_run(conn, scrape_run_id, records_found):
    with conn.cursor as cursor:
        cursor.execute(
            """
            UPDATE raw.scrape_runs
            SET 
                finished_at = NOW(),
                status = 'success',
                records_found = %s
            WHERE id = %s;
            """,
            (
                records_found,
                scrape_run_id,
            ),
        )

def fail_scrape_run(conn, scrape_run_id, error_message):
    with conn.cursor as cursor:
        cursor.execute(
            """
            UPDATE raw.scrape_runs
            SET
                finished_at = NOW(),
                status = 'failed',
                error_message = %s
            WHERE id = %s;
            """,
            (
                str(error_message),
                scrape_run_id,
            ),
        )