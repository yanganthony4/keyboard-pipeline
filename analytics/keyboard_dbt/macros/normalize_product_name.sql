{% macro normalize_product_name(column_name) %}

trim(
    regexp_replace(
        lower({{ column_name }}),
        '[^a-z0-9]+',
        ' ',
        'g'
    )
)

{% endmacro %}

