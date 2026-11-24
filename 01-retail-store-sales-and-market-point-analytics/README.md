# Retail Store-Point Sales & Commercial Analytics

**Python (`Pandas`, `NumPy`, `SciPy`) | PostgreSQL / SQL | Retail KPI Reporting**

---

## Project Overview

An end-to-end retail analytics pipeline designed to evaluate multi-store sales performance, market-point revenue contribution, product assortment stability, and promotional campaign effectiveness.

## Key Analytical Modules

1. **Data Cleaning & Enrichment:** Deduplication, SKU-level median price imputation, net revenue, COGS, and gross margin engineering.
2. **Store / Market-Point Benchmarking:** Revenue share, transaction volume, average basket value, and profitability comparison across retail points.
3. **Time-Series & MoM Growth Tracking:** Monthly revenue dynamics and month-over-month percentage growth analysis.
4. **ABC-XYZ Assortment Segmentation:** Combining Pareto revenue contribution (`A/B/C`) with demand volatility (`X/Y/Z` via Coefficient of Variation) to optimize stock allocation.
5. **Promotional Impact Testing:** Two-sample Welch's t-test comparing promotional vs. regular transaction basket values.

## Repository Structure

```text
01-retail-store-sales-and-market-point-analytics/
├── retail_sales_market_analytics.py
├── retail_store_kpis.sql
└── README.md
```

## Author

**Aysu Gadirova** — Data Analyst
