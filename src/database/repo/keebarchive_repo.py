from src.database.raw import (
    create_scrape_run,
    create_source_record,
    complete_scrape_run,
    fail_scrape_run,
)
from src.database.connection import get_connection

def create_switch_record(
        conn,
        record_id,
        switch_type,
        feel,
        actuation_force,
        travel_distance,
        pins,
        factory_lubed,
):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO raw.keebarchive_switches(
                record_id,
                switch_type,
                feel,
                actuation_force,
                travel_distance,
                pins,
                factory_lubed
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s
            )
            ON CONFLICT (record_id)
            DO NOTHING;
            """,
            (
                record_id,
                switch_type,
                feel,
                actuation_force,
                travel_distance,
                pins,
                factory_lubed
            )
        )

def create_keycap_record(
        conn,
        record_id,
        material,
        keycap_profile,
        number_of_keys,
        artisan
):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO raw.keebarchive_keycaps(
                record_id,
                material,
                keycap_profile,
                number_of_keys,
                artisan
            )
            VALUES (
                %s, %s, %s, %s, %s
            )
            ON CONFLICT (record_id)
            DO NOTHING;
            """,
            (
                record_id,
                material,
                keycap_profile,
                number_of_keys,
                artisan
            )
        )

def save_switches(switches):
    with get_connection() as conn:
        scrape_run_id = create_scrape_run(conn, "keebarchive switches")

        print(f"Storing scrape {scrape_run_id}: Keebarchive Switches")

        conn.commit()

        try:
            for switch in switches:
                record_id = create_source_record(
                    conn=conn,
                    scrape_run_id=scrape_run_id,
                    record_type="switch",
                    source_url=switch["source_url"],
                    vendor_url=switch.get("vendor_url"),
                    source_product_id=switch.get("source_product_id"),
                    title=switch["title"],
                    price=switch.get("price"),
                    prose=switch.get("prose"),
                    raw_specifications=switch.get(
                        "raw_specifications",
                        []
                    ),
                )

                create_switch_record(
                    conn=conn,
                    record_id=record_id,
                    switch_type=switch.get("switch_type"),
                    feel=switch.get("feel"),
                    actuation_force=switch.get("actuation_force"),
                    travel_distance=switch.get("travel_distance"),
                    pins=switch.get("pins"),
                    factory_lubed=switch.get("factory_lubed"),
                )
            
            complete_scrape_run(
                conn,
                scrape_run_id,
                len(switches)
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

def save_keycaps(keycaps):
    with get_connection() as conn:
        scrape_run_id = create_scrape_run(conn, "keebarchive keycaps")

        print(f"Storing scrape {scrape_run_id}: Keebarchive Kecyaps")

        conn.commit()

        try:
            for keycap in keycaps:
                record_id = create_source_record(
                    conn=conn,
                    scrape_run_id=scrape_run_id,
                    record_type="keycap",
                    source_url=keycap["source_url"],
                    vendor_url=keycap.get("vendor_url"),
                    source_product_id=keycap.get("source_product_id"),
                    title=keycap["title"],
                    price=keycap.get("price"),
                    prose=keycap.get("prose"),
                    raw_specifications=keycap.get(
                        "raw_specifications",
                        []
                    ),
                )

                create_keycap_record(
                    conn=conn,
                    record_id=record_id,
                    material=keycap.get("material"),
                    keycap_profile=keycap.get("keycap_profile"),
                    number_of_keys=keycap.get("number_of_keys"),
                    artisan=keycap.get("artisan")
                )
            
            complete_scrape_run(
                conn,
                scrape_run_id,
                len(keycaps)
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