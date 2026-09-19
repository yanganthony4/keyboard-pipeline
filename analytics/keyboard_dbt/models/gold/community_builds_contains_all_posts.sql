select
    r.source_post_id

from {{ ref('stg_reddit_posts') }} as r

left join {{ ref('community_builds') }} as b
    on r.source_post_id = b.source_post_id

where b.source_post_id is null