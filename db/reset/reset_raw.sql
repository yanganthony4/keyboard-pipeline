-- Get-Content .\db\reset\reset_raw.sql -Raw | docker exec -i keyboard-postgres psql -v ON_ERROR_STOP=1 -U keyboard_admin -d keyboard_db

DROP TABLE IF EXISTS raw.keebarchive_switches;
DROP TABLE IF EXISTS raw.keebarchive_keycaps;
DROP TABLE IF EXISTS raw.keebfinder_keyboards;
DROP TABLE IF EXISTS raw.reddit_posts;
DROP TABLE IF EXISTS raw.source_records;
DROP TABLE IF EXISTS raw.scrape_runs;


CREATE TABLE raw.scrape_runs (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    source TEXT NOT NULL,

    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    finished_at TIMESTAMPTZ,

    status TEXT NOT NULL DEFAULT 'running',
    records_found INTEGER,
    error_message TEXT,

    CONSTRAINT scrape_runs_status_check
        CHECK (status IN ('running', 'success', 'failed'))
);


CREATE TABLE raw.source_records (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    scrape_run_id BIGINT NOT NULL,
    record_type TEXT NOT NULL,

    source_url TEXT NOT NULL,
    vendor_url TEXT,
    source_product_id TEXT,

    extracted_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    title TEXT NOT NULL,
    price TEXT,
    prose TEXT,

    raw_specifications JSONB,

    CONSTRAINT source_records_scrape_run_fk
        FOREIGN KEY (scrape_run_id)
        REFERENCES raw.scrape_runs(id),

    CONSTRAINT source_records_type_check
    CHECK (
        record_type IN (
            'switch',
            'keycap',
            'keyboard'
        )
    ), 

    CONSTRAINT source_records_run_url_unique
        UNIQUE(scrape_run_id, source_url)
);


CREATE TABLE raw.keebarchive_switches (
    record_id BIGINT PRIMARY KEY,

    switch_type TEXT,
    feel TEXT,
    actuation_force TEXT,
    travel_distance TEXT,
    pins INTEGER,
    factory_lubed BOOLEAN,

    CONSTRAINT keebarchive_switches_record_fk
        FOREIGN KEY (record_id)
        REFERENCES raw.source_records(id)
);


CREATE TABLE raw.keebarchive_keycaps (
    record_id BIGINT PRIMARY KEY,

    material TEXT,
    keycap_profile TEXT,
    number_of_keys INTEGER,
    artisan BOOLEAN,

    CONSTRAINT keebarchive_keycaps_record_fk
        FOREIGN KEY (record_id)
        REFERENCES raw.source_records(id)
);


CREATE TABLE raw.keebfinder_keyboards (
    record_id BIGINT PRIMARY KEY,

    keyboard_profile TEXT,
    wired BOOLEAN,
    wireless BOOLEAN,
    hotswap BOOLEAN,
    rgb BOOLEAN,
    white_led BOOLEAN,
    knob BOOLEAN,
    hall_effect BOOLEAN,
    rapid_trigger BOOLEAN,
    metal_case BOOLEAN,
    mount TEXT,
    via_support BOOLEAN,
    qmk_support BOOLEAN,

    CONSTRAINT keebfinder_keyboards_record_fk
        FOREIGN KEY (record_id)
        REFERENCES raw.source_records(id)
);

CREATE TABLE raw.reddit_posts (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    scrape_run_id BIGINT NOT NULL,

    post_url TEXT NOT NULL,
    extracted_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    subreddit TEXT NOT NULL,
    source_post_id TEXT NOT NULL,
    title TEXT NOT NULL,
    body TEXT,
    author TEXT,
    created_at TIMESTAMPTZ,
    gallery_images JSONB,
    author_comments JSONB,

    CONSTRAINT reddit_posts_scrape_run_fk
        FOREIGN KEY (scrape_run_id)
        REFERENCES raw.scrape_runs(id),

    CONSTRAINT reddit_posts_run_post_unique
        UNIQUE (scrape_run_id, source_post_id)
);