select
    source_post_id,
    post_url,
    normalized_searchable_text

from {{ ref('stg_reddit_posts') }}

where normalized_searchable_text is not null