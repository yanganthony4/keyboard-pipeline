select *
from {{ ref('product_aliases') }}
where trim(alias) = ''