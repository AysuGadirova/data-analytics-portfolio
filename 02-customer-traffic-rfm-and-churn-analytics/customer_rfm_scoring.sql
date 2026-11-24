-- Customer RFM Scoring in SQL using NTILE Window Functions
WITH customer_metrics AS (
    SELECT
        customer_id,
        CURRENT_DATE - MAX(visit_date)::date AS recency_days,
        COUNT(visit_id) AS frequency,
        SUM(spend_azn) AS monetary_value
    FROM customer_visits
    GROUP BY customer_id
),
rfm_scores AS (
    SELECT
        customer_id,
        recency_days,
        frequency,
        ROUND(monetary_value, 2) AS monetary_value,
        NTILE(4) OVER (ORDER BY recency_days DESC) AS r_score,
        NTILE(4) OVER (ORDER BY frequency ASC) AS f_score,
        NTILE(4) OVER (ORDER BY monetary_value ASC) AS m_score
    FROM customer_metrics
)
SELECT
    customer_id,
    recency_days,
    frequency,
    monetary_value,
    (r_score + f_score + m_score) AS total_rfm_score,
    CASE
        WHEN r_score >= 3 AND f_score >= 3 AND m_score >= 3 THEN 'Champions'
        WHEN r_score <= 2 AND f_score >= 3 THEN 'At Risk'
        WHEN r_score = 1 THEN 'Churned'
        ELSE 'Regular / Growth'
    END AS customer_segment
FROM rfm_scores
ORDER BY total_rfm_score DESC, monetary_value DESC;
