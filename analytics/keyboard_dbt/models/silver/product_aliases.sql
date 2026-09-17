with canonical_aliases as (

    select
        product_id,
        product_type,
        title as canonical_title,
        normalized_title as alias,
        'canonical' as alias_type

    from {{ ref('products') }}

),

manual_aliases as (

    select
        p.product_id,
        p.product_type,
        p.title as canonical_title,
        {{ normalize_product_name('a.alias') }} as alias,
        'manual' as alias_type

    from {{ ref('manual_product_aliases') }} as a

    join {{ ref('products') }} as p
        on a.product_type = p.product_type
        and a.canonical_normalized_title = p.normalized_title

)

select * from canonical_aliases

union all

select * from manual_aliases