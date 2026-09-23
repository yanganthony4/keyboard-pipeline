with product_builds as (

    select
        product_id,

        jsonb_agg(
            jsonb_build_object(
                'source_post_id', source_post_id,
                'post_url', post_url,
                'match_score', match_score
            )
            order by match_score desc
        ) as community_builds

    from {{ ref('product_builds') }}

    group by product_id

),

switches as (

    select
        p.product_id,
        p.product_type,
        p.title,
        p.normalized_title,
        p.source_url,
        p.vendor_url,
        p.source_product_id,

        s.price_amount,
        s.price_currency,

        jsonb_build_object(
            'switch_type', s.switch_type,
            'switch_feel', s.switch_feel,
            'actuation_force_gf', s.actuation_force_gf,
            'actuation_force_tolerance_gf', s.actuation_force_tolerance_gf,
            'travel_distance_mm', s.travel_distance_mm,
            'pins', s.pins,
            'factory_lubed', s.factory_lubed
        ) as specifications,

        coalesce(
            pb.community_builds,
            '[]'::jsonb
        ) as community_builds

    from {{ ref('products') }} as p

    join {{ ref('stg_switches') }} as s
        on p.product_id = s.record_id

    left join product_builds as pb
        on p.product_id = pb.product_id

    where p.product_type = 'switch'

),

keycaps as (

    select
        p.product_id,
        p.product_type,
        p.title,
        p.normalized_title,
        p.source_url,
        p.vendor_url,
        p.source_product_id,

        k.price_amount,
        k.price_currency,

        jsonb_build_object(
            'material', k.material,
            'keycap_profile', k.keycap_profile,
            'number_of_keys', k.number_of_keys,
            'artisan', k.artisan
        ) as specifications,

        coalesce(
            pb.community_builds,
            '[]'::jsonb
        ) as community_builds

    from {{ ref('products') }} as p

    join {{ ref('stg_keycaps') }} as k
        on p.product_id = k.record_id

    left join product_builds as pb
        on p.product_id = pb.product_id

    where p.product_type = 'keycap'

),

keyboards as (

    select
        p.product_id,
        p.product_type,
        p.title,
        p.normalized_title,
        p.source_url,
        p.vendor_url,
        p.source_product_id,

        k.price_amount,
        k.price_currency,

        jsonb_build_object(
            'keyboard_profile', k.keyboard_profile_text,
            'keyboard_profile_percent', k.keyboard_profile_percent,
            'wired', k.wired,
            'wireless', k.wireless,
            'hotswap', k.hotswap,
            'rgb', k.rgb,
            'white_led', k.white_led,
            'knob', k.knob,
            'hall_effect', k.hall_effect,
            'rapid_trigger', k.rapid_trigger,
            'metal_case', k.metal_case,
            'mount', k.mount,
            'via_support', k.via_support,
            'qmk_support', k.qmk_support
        ) as specifications,

        coalesce(
            pb.community_builds,
            '[]'::jsonb
        ) as community_builds

    from {{ ref('products') }} as p

    join {{ ref('stg_keyboards') }} as k
        on p.product_id = k.record_id

    left join product_builds as pb
        on p.product_id = pb.product_id

    where p.product_type = 'keyboard'

)

select * from switches

union all

select * from keycaps

union all

select * from keyboards