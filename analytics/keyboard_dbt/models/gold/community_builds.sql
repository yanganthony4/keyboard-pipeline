with builds as (

    select
        id,
        source_post_id,
        post_url,
        subreddit,
        title,
        body,
        author,
        created_at,
        gallery_images,
        author_comments

    from {{ ref('stg_reddit_posts') }}

),

keyboard_matches as (

    select
        source_post_id,

        jsonb_agg(
            jsonb_build_object(
                'product_id', product_id,
                'title', canonical_title,
                'match_score', match_score
            )
            order by match_score desc
        ) as keyboards

    from {{ ref('reddit_product_match_candidates') }}

    where product_type = 'keyboard'

    group by source_post_id

),

switch_matches as (

    select
        source_post_id,

        jsonb_agg(
            jsonb_build_object(
                'product_id', product_id,
                'title', canonical_title,
                'match_score', match_score
            )
            order by match_score desc
        ) as switches

    from {{ ref('reddit_product_match_candidates') }}

    where product_type = 'switch'

    group by source_post_id

),

keycap_matches as (

    select
        source_post_id,

        jsonb_agg(
            jsonb_build_object(
                'product_id', product_id,
                'title', canonical_title,
                'match_score', match_score
            )
            order by match_score desc
        ) as keycaps

    from {{ ref('reddit_product_match_candidates') }}

    where product_type = 'keycap'

    group by source_post_id

)

select
    b.id,
    b.source_post_id,
    b.post_url,
    b.subreddit,
    b.title,
    b.body,
    b.author,
    b.created_at,
    b.gallery_images,
    b.author_comments,

    coalesce(
        k.keyboards,
        '[]'::jsonb
    ) as keyboards,

    coalesce(
        s.switches,
        '[]'::jsonb
    ) as switches,

    coalesce(
        c.keycaps,
        '[]'::jsonb
    ) as keycaps

from builds as b

left join keyboard_matches as k
    on b.source_post_id = k.source_post_id

left join switch_matches as s
    on b.source_post_id = s.source_post_id

left join keycap_matches as c
    on b.source_post_id = c.source_post_id