select
    product_id,
    source_post_id,
    count(*) as match_count

from {{ ref('product_builds') }}

group by
    product_id,
    source_post_id

having count(*) > 1