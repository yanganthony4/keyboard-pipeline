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
                travel
            )
            VALUES (
                %s, %s, %s, %s, %s
            )
            RETURNING id;
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
                %s, %s, %s, %s, $s,
            )
            RETURNING id;
            """,
            (
                record_id,
                material,
                keycap_profile,
                number_of_keys,
                artisan
            )
        )