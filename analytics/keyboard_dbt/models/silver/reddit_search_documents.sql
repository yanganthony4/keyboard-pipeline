{{ config(
    post_hook="
        create index if not exists reddit_search_documents_trgm_idx
        on {{ this }}
        using gin (normalized_searchable_text gin_trgm_ops)
    "
) }}

select
    source_post_id,
    post_url,
    normalized_searchable_text

from {{ ref('stg_reddit_posts') }}

where normalized_searchable_text is not null