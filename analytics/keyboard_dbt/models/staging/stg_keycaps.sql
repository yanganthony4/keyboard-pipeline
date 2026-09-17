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

    nullif(lower(trim(k.material)), '') as material,
    nullif(lower(trim(k.keycap_profile)), '') as keycap_profile,
    k.number_of_keys,
    k.artisan
from {{ source('raw', 'keebarchive_keycaps') }} as k
join {{ source('raw', 'source_records') }} as r
    on k.record_id = r.id
where nullif(trim(r.title), '') is not null
    and r.record_type = 'keycap'
