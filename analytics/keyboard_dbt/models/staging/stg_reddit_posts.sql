select
    id,
    post_url,
    
    subreddit,
    source_post_id,
    
    regexp_replace(trim(title), '\s+', ' ', 'g') as title,
    trim(body) as body_text,
    nullif(
        regexp_replace(
            trim(body),
            '\s+',
            ' ',
            'g'
        ),
        ''
    ) as body,
    author,
    created_at,
    gallery_images,
    author_comments
from {{ source('raw', 'reddit_posts') }} 

    
