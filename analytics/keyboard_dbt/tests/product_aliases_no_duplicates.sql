select
    product_id,
    alias,
    count(*) as alias_count

from {{ ref('product_aliases') }}

group by
    product_id,
    alias

having count(*) > 1