-- Retail Store-Point Monthly Revenue, MoM Growth & Pareto 80/20 Queries
WITH monthly_store_sales AS (
    SELECT
        store_id,
        DATE_TRUNC('month', transaction_date) AS sales_month,
        COUNT(DISTINCT transaction_id) AS total_orders,
        SUM(units_sold * effective_price) AS monthly_revenue,
        SUM(gross_profit) AS monthly_profit
    FROM retail_sales
    GROUP BY store_id, DATE_TRUNC('month', transaction_date)
)
SELECT
    store_id,
    sales_month,
    total_orders,
    ROUND(monthly_revenue, 2) AS monthly_revenue,
    ROUND(
        (monthly_revenue - LAG(monthly_revenue) OVER (PARTITION BY store_id ORDER BY sales_month))
        / NULLIF(LAG(monthly_revenue) OVER (PARTITION BY store_id ORDER BY sales_month), 0) * 100,
        2
    ) AS mom_growth_pct,
    DENSE_RANK() OVER (PARTITION BY sales_month ORDER BY monthly_revenue DESC) AS store_rank_in_month
FROM monthly_store_sales
ORDER BY sales_month DESC, store_rank_in_month ASC;
