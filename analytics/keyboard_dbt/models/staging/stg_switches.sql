select
    s.record_id,

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

    nullif(lower(trim(s.switch_type)), '') as switch_type,
    nullif(lower(trim(s.feel)), '') as switch_feel,
    
    nullif(lower(trim(s.actuation_force)), '') as actuation_force_text,
    ((regexp_match(s.actuation_force, '([0-9]+(?:\.[0-9]+)?)'))[1])::numeric
    as actuation_force_gf,
    ((regexp_match(s.actuation_force, '±\s*([0-9]+(?:\.[0-9]+)?)'))[1])::numeric
    as actuation_force_tolerance_gf,

    nullif(lower(trim(s.travel_distance)), '') as travel_distance_text,
    ((regexp_match(s.travel_distance,'([0-9]+(?:\.[0-9]+)?)'))[1])::numeric as travel_distance_mm,
    
    s.pins, 
    s.factory_lubed
from {{ source('raw', 'keebarchive_switches') }} as s
join {{ source('raw', 'source_records') }} as r
    on s.record_id = r.id
where nullif(trim(r.title), '') is not null
    and r.record_type = 'switch'
