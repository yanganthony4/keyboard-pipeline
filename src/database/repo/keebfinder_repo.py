from src.database.raw import (
    create_scrape_run,
    create_source_record,
    complete_scrape_run,
    fail_scrape_run,
)
from src.database.connection import get_connection


def create_keyboard_record(
    conn,
    record_id,
    keyboard_profile,
    wired,
    wireless,
    hotswap,
    rgb,
    white_led,
    knob,
    hall_effect,
    rapid_trigger,
    metal_case,
    mount,
    via_support,
    qmk_support,
):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO raw.keebfinder_keyboards (
                record_id,
                keyboard_profile,
                wired,
                wireless,
                hotswap,
                rgb,
                white_led,
                knob,
                hall_effect,
                rapid_trigger,
                metal_case,
                mount,
                via_support,
                qmk_support
            )
            VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s
            )
            ON CONFLICT (record_id)
            DO NOTHING;
            """,
            (
                record_id,
                keyboard_profile,
                wired,
                wireless,
                hotswap,
                rgb,
                white_led,
                knob,
                hall_effect,
                rapid_trigger,
                metal_case,
                mount,
                via_support,
                qmk_support,
            ),
        )


def save_keyboards(keyboards):
    with get_connection() as conn:
        scrape_run_id = create_scrape_run(conn, "keebfinder")

        print(f"Storing scrape {scrape_run_id}: keebfinder keyboards")

        # Preserve evidence that this scrape run occurred.
        conn.commit()

        try:
            for keyboard in keyboards:
                record_id = create_source_record(
                    conn=conn,
                    scrape_run_id=scrape_run_id,
                    record_type="keyboard",
                    source_url=keyboard["source_url"],
                    vendor_url=keyboard.get("vendor_url"),
                    source_product_id=keyboard.get("source_product_id"),
                    title=keyboard["title"],
                    price=keyboard.get("price"),
                    prose=keyboard.get("prose"),
                    raw_specifications=keyboard.get(
                        "raw_specifications",
                        []
                    ),
                )

                create_keyboard_record(
                    conn=conn,
                    record_id=record_id,
                    keyboard_profile=keyboard.get("keyboard_profile"),
                    wired=keyboard.get("wired"),
                    wireless=keyboard.get("wireless"),
                    hotswap=keyboard.get("hotswap"),
                    rgb=keyboard.get("rgb"),
                    white_led=keyboard.get("white_led"),
                    knob=keyboard.get("knob"),
                    hall_effect=keyboard.get("hall_effect"),
                    rapid_trigger=keyboard.get("rapid_trigger"),
                    metal_case=keyboard.get("metal_case"),
                    mount=keyboard.get("mount"),
                    via_support=keyboard.get("via_support"),
                    qmk_support=keyboard.get("qmk_support"),
                )

            complete_scrape_run(
                conn,
                scrape_run_id,
                len(keyboards),
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