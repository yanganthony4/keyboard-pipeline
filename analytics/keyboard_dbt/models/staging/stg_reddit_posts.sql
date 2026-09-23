with reddit_posts as (

    select
        r.*,

        row_number() over (
            partition by r.source_post_id
            order by r.extracted_at desc, r.id desc
        ) as row_num

    from {{ source('raw', 'reddit_posts') }} as r

)

select
    r.id,
    r.post_url,

    r.subreddit,
    r.source_post_id,

    regexp_replace(
        trim(r.title),
        '\s+',
        ' ',
        'g'
    ) as title,

    trim(r.body) as body_text,

    nullif(
        regexp_replace(
            trim(r.body),
            '\s+',
            ' ',
            'g'
        ),
        ''
    ) as body,

    r.author,
    r.created_at,
    r.gallery_images,
    r.author_comments,

    lower(
        regexp_replace(
            trim(
                concat_ws(
                    ' ',
                    r.title,
                    r.body,
                    comments.comment_text
                )
            ),
            '\s+',
            ' ',
            'g'
        )
    ) as normalized_searchable_text

from reddit_posts as r
left join lateral (

    select
        string_agg(comment, ' ') as comment_text

    from jsonb_array_elements_text(r.author_comments) as comment

) as comments
    on true
where r.row_num = 1
