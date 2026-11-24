# Multi-Table Customer & Portfolio Risk Analytics (Python)

**Python (`Pandas`, `NumPy`, `Matplotlib`, `Seaborn`) | Data Cleaning, Statistical Outliers & Risk Segmentation**

---

## Project Overview

An end-to-end Python analytics notebook integrating four relational business tables (`customers`, `policies`, `claims`, and `payments`) to assess portfolio profitability, payment behavior, statistical outliers, and customer/policy risk tiers.

## Analytical Workflow

1. **Automated Data Quality & Validation:** Duplicate checks, datetime standardization, null handling, and business-rule validation (`join_date >= birth_date`).
2. **Relational Data Modeling:** Aggregating claim and payment histories per entity and merging into a unified analytical master table.
3. **Portfolio KPI Computation:** Calculating total revenue/premiums, claim/payout ratios, and customer renewal rates.
4. **IQR Outlier Detection & Visual EDA:** Identifying extreme financial transactions using the Interquartile Range (IQR) method and distribution boxplots.
5. **Risk & Value Segmentation:** Classifying active accounts into Low-, Medium-, and High-Risk tiers to guide retention and pricing strategy.

## Repository Structure

```text
05-portfolio-risk-and-customer-segmentation-python/
├── Customer_Portfolio_Analytics_Aysu_Gadirova.ipynb
├── data-analyst-task-datasets.xlsx
└── README.md
```

## Author

**Aysu Gadirova** — Data Analyst
