
select
    date(order_purchase_ts) as order_date,
    count(distinct order_id) as total_orders,
    sum(total_order_item_value) as total_revenue

from {{ ref('fct_order_items') }}

group by 1
order by 1