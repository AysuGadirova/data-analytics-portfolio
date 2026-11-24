# Customer Traffic, RFM Segmentation & Churn Analytics

**Python (`Pandas`, `NumPy`, `Scikit-Learn`) | SQL | Customer Retention & Growth**

---

## Project Overview

A customer database and behavioral analytics project focused on increasing customer foot traffic, improving repeat visit frequency, and identifying churn risk across acquisition channels.

## Key Analytical Modules

1. **RFM Customer Segmentation:** Scoring customers across Recency, Frequency, and Monetary value to classify high-value segments (*Champions*, *Loyal Customers*, *At-Risk High Value*, *Hibernating*).
2. **Cohort Retention Matrix:** Tracking monthly customer return rates from initial visit month (`Cohort Index 0..N`) to evaluate long-term engagement.
3. **Predictive Churn Modeling:** Training a `RandomForestClassifier` evaluated via `ROC-AUC` and classification metrics to flag customers at risk of churn (>90 days inactivity).
4. **SQL RFM Scoring:** Production-ready PostgreSQL query utilizing `NTILE()` window functions for automated CRM segmentation.

## Repository Structure

```text
02-customer-traffic-rfm-and-churn-analytics/
├── customer_rfm_churn_analytics.py
├── customer_rfm_scoring.sql
└── README.md
```

## Author

**Aysu Gadirova** — Data Analyst
