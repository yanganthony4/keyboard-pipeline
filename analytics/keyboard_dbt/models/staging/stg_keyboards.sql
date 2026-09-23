select
    k.record_id,

    trim(r.title) as title,
    {{ normalize_product_name('r.title') }} as normalized_title,

    r.scrape_run_id,
    r.source_url,
    r.vendor_url,
    r.source_product_id,
    r.extracted_at,

    nullif(lower(trim(r.price)), '') as price_text,
    ((regexp_match(r.price, '([0-9]+(?:\.[0-9]+)?)'))[1])::numeric as price_amount,
    case
        when nullif(trim(r.price), '') is not null then 'USD'
        else null
    end as price_currency,

    nullif(trim(r.prose), '') as prose,

    nullif(trim(k.keyboard_profile), '') as keyboard_profile_text,
    (
        (regexp_match(
            k.keyboard_profile,
            '([0-9]+(?:\.[0-9]+)?)\s*%'
        ))[1]
    )::numeric as keyboard_profile_percent,

    k.wired,
    k.wireless,
    k.hotswap,
    k.rgb,
    k.white_led,
    k.knob,
    k.hall_effect,
    k.rapid_trigger,
    k.metal_case,
    nullif(lower(trim(k.mount)), '') as mount,
    k.via_support,
    k.qmk_support
from {{ source('raw', 'keebfinder_keyboards') }} as k
join {{ source('raw', 'source_records') }} as r
    on k.record_id = r.id
where nullif(trim(r.title), '') is not null
    and r.record_type = 'keyboard'
