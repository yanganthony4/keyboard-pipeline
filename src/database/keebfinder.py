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
        qmk_support
):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO raw.keebarchive_keycaps(
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
                %s, %s, %s, %s, $s, 
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s
            )
            RETURNING id;
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
                qmk_support
            )
        )