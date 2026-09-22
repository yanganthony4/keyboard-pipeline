{{ config(
    materialized='incremental',
    unique_key='source_post_id',
    incremental_strategy='delete+insert',
    post_hook="
        create index if not exists reddit_search_documents_trgm_idx
        on {{ this }}
        using gin (normalized_searchable_text gin_trgm_ops)
    "
) }}

{% set scrape_run_id = var('scrape_run_id', none) %}

select
    source_post_id,
    scrape_run_id,
    post_url,
    normalized_searchable_text

from {{ ref('stg_reddit_posts') }}

where normalized_searchable_text is not null

{% if scrape_run_id is not none %}

    and scrape_run_id = {{ scrape_run_id }}

{% endif %}