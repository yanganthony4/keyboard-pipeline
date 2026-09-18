with canonical_aliases as (

    select
        product_id,
        product_type,
        title as canonical_title,
        normalized_title as alias,
        'canonical' as alias_type

    from {{ ref('products') }}

),

generated_switch_aliases_raw as (

    select
        product_id,
        product_type,
        title as canonical_title,
        normalized_title,

        trim(
            regexp_replace(
                regexp_replace(
                    regexp_replace(
                        regexp_replace(
                            normalized_title,
                            '[0-9]+( [0-9]+)?g',
                            ' ',
                            'g'
                        ),
                        '\m(low profile|plate mount|pcb mount|linear|tactile|clicky|magnetic|he|switches|switch)\M',
                        ' ',
                        'g'
                    ),
                    '[0-9]+ pack',
                    ' ',
                    'g'
                ),
                '\s+',
                ' ',
                'g'
            )
        ) as alias

    from {{ ref('products') }}

    where product_type = 'switch'
),

generated_switch_aliases as (

    select
        product_id,
        product_type,
        canonical_title,
        alias,
        'generated' as alias_type

    from generated_switch_aliases_raw

    where alias <> normalized_title
      and alias <> ''

),

generated_keycap_aliases_raw as (

    select
        product_id,
        product_type,
        title as canonical_title,
        normalized_title,

        trim(
            regexp_replace(
                regexp_replace(
                    regexp_replace(
                        normalized_title,
                        '[0-9]+ key',
                        ' ',
                        'g'
                    ),
                    '\m(cherry profile|sa profile|mda profile|oem profile|artisan|keycaps set|keycap set|keycaps|keycap)\M',
                    ' ',
                    'g'
                ),
                '\s+',
                ' ',
                'g'
            )
        ) as alias

    from {{ ref('products') }}

    where product_type = 'keycap'
),

generated_keycap_aliases as (

    select
        product_id,
        product_type,
        canonical_title,
        alias,
        'generated' as alias_type

    from generated_keycap_aliases_raw

    where alias <> normalized_title
      and alias <> ''

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

select * from generated_switch_aliases

union all

select * from generated_keycap_aliases

union all

select * from manual_aliases