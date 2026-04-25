
select
    product_id,
    product_category_name,

    cast(product_name_lenght as int) as product_name_length,
    cast(product_description_lenght as int) as product_description_length,
    cast(product_photos_qty as int) as product_photos_qty,

    cast(product_weight_g as numeric) as product_weight_g,
    cast(product_length_cm as numeric) as product_length_cm,
    cast(product_height_cm as numeric) as product_height_cm,
    cast(product_width_cm as numeric) as product_width_cm

from {{ source('raw', 'products') }}