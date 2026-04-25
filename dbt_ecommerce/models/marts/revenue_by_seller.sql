
select
    s.seller_id,
    s.seller_state,
    sum(f.total_order_item_value) as total_revenue

from {{ ref('fct_order_items') }} f
join {{ ref('dim_sellers') }} s
    on f.seller_id = s.seller_id

group by 1,2
order by 3 desc