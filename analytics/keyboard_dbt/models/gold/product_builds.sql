select
    product_id,
    product_type,
    canonical_title,
    source_post_id,
    post_url,
    match_score

from {{ ref('reddit_product_match_candidates') }}