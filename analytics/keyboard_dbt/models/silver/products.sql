with switches as (

    select
        record_id as product_id,
        'switch' as product_type,
        title,
        normalized_title,
        source_url,
        vendor_url,
        source_product_id,
        extracted_at

    from {{ ref('stg_switches') }}

),

keycaps as (

    select
        record_id as product_id,
        'keycap' as product_type,
        title,
        normalized_title,
        source_url,
        vendor_url,
        source_product_id,
        extracted_at

    from {{ ref('stg_keycaps') }}

),

keyboards as (

    select
        record_id as product_id,
        'keyboard' as product_type,
        title,
        normalized_title,
        source_url,
        vendor_url,
        source_product_id,
        extracted_at

    from {{ ref('stg_keyboards') }}

)

select * from switches

union all

select * from keycaps

union all

select * from keyboards