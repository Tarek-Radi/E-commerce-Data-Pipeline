
select
    p.product_category_name_english as category,
    sum(f.total_order_item_value) as total_revenue

from {{ ref('fct_order_items') }} f
join {{ ref('dim_products') }} p
    on f.product_id = p.product_id

group by 1
order by 2 desc