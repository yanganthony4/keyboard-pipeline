{{ config(
    materialized='incremental',
    unique_key=['source_post_id', 'product_id'],
    incremental_strategy='delete+insert'
) }}

{% set scrape_run_id = var('scrape_run_id', none) %}

with posts as (
    select
        source_post_id,
        post_url,
        normalized_searchable_text
    from {{ ref('reddit_search_documents') }}

    {% if scrape_run_id is not none %}

    where scrape_run_id = {{ scrape_run_id }}

    {% endif %}
),

aliases as (
    select
        product_id,
        product_type,
        canonical_title,
        alias,
        alias_type
    from {{ ref('product_aliases') }}
),

candidates as (
    select
        p.source_post_id,
        p.scrape_run_id,
        p.post_url,
        a.product_id,
        a.product_type,
        a.canonical_title,
        a.alias,
        a.alias_type,

        word_similarity(
            a.alias,
            p.normalized_searchable_text
        ) as match_score
    from aliases as a

    join posts as p
        on a.alias <% p.normalized_searchable_text
),

ranked_candidates as (

    select
        *,
        row_number() over (
            partition by source_post_id, product_id
            order by match_score desc
        ) as match_rank

    from candidates

)

select *
from ranked_candidates
where match_score = 1