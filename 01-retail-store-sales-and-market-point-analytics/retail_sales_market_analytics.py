"""
================================================================================
PROJECT 01: RETAIL & STORE-POINT SALES ANALYTICS
Author: Aysu Gadirova | Data Analyst
Domain: Multi-Store Retail Operations & Commercial Reporting
Tech Stack: Python (Pandas, NumPy, SciPy), PostgreSQL / SQL
================================================================================
"""

import numpy as np
import pandas as pd
from scipy import stats

# 1. DATA GENERATION (SIMULATED MULTI-STORE RETAIL DATASET)
np.random.seed(42)
n_transactions = 15000
stores = ["Baku_Center_01", "Ganjlik_Mall_02", "28_Mall_03", "Narimanov_04", "Yasamal_05"]
categories = ["Electronics", "FMCG_Food", "Cosmetics", "Home_Goods", "Accessories"]
products = [f"SKU_{i:03d}" for i in range(1, 51)]
dates = pd.date_range(start="2025-01-01", end="2026-10-31", freq="D")

df_sales = pd.DataFrame({
    "transaction_id": [f"TRX-{100000 + i}" for i in range(n_transactions)],
    "date": np.random.choice(dates, size=n_transactions),
    "store_id": np.random.choice(stores, size=n_transactions, p=[0.28, 0.25, 0.22, 0.15, 0.10]),
    "category": np.random.choice(categories, size=n_transactions),
    "sku": np.random.choice(products, size=n_transactions),
    "units_sold": np.random.poisson(lam=3, size=n_transactions) + 1,
    "unit_price": np.round(np.random.uniform(5.0, 180.0, size=n_transactions), 2),
    "cost_ratio": np.random.uniform(0.55, 0.78, size=n_transactions),
    "is_promo": np.random.choice([0, 1], size=n_transactions, p=[0.75, 0.25])
})

# Inject realistic missing values & duplicates for data quality pipeline
df_sales.loc[np.random.choice(df_sales.index, 120, replace=False), "unit_price"] = np.nan
df_sales = pd.concat([df_sales, df_sales.iloc[:50]], ignore_index=True)

# 2. DATA CLEANING & FEATURE ENGINEERING
def clean_and_enrich_sales(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop_duplicates(subset=["transaction_id"]).copy()
    df["unit_price"] = df["unit_price"].fillna(
        df.groupby("sku")["unit_price"].transform("median")
    )
    df["effective_price"] = np.where(df["is_promo"] == 1, df["unit_price"] * 0.85, df["unit_price"])
    df["revenue"] = np.round(df["units_sold"] * df["effective_price"], 2)
    df["cogs"] = np.round(df["units_sold"] * df["unit_price"] * df["cost_ratio"], 2)
    df["gross_profit"] = np.round(df["revenue"] - df["cogs"], 2)
    df["margin_pct"] = np.round((df["gross_profit"] / df["revenue"]) * 100, 2)
    df["date"] = pd.to_datetime(df["date"])
    df["year_month"] = df["date"].dt.to_period("M")
    df["day_of_week"] = df["date"].dt.day_name()
    return df

df_clean = clean_and_enrich_sales(df_sales)

# 3. STORE / MARKET POINT KPI PERFORMANCE
store_kpi = (
    df_clean.groupby("store_id")
    .agg(
        total_transactions=("transaction_id", "count"),
        total_units=("units_sold", "sum"),
        total_revenue=("revenue", "sum"),
        total_profit=("gross_profit", "sum"),
        avg_basket_value=("revenue", "mean"),
        avg_margin_pct=("margin_pct", "mean")
    )
    .sort_values(by="total_revenue", ascending=False)
    .reset_index()
)
store_kpi["revenue_share_pct"] = np.round(
    store_kpi["total_revenue"] / store_kpi["total_revenue"].sum() * 100, 2
)

print("=== STORE / MARKET POINT KPI SUMMARY ===")
print(store_kpi.to_string(index=False))

# 4. MONTHLY SALES TREND & MoM GROWTH
monthly_trend = (
    df_clean.groupby("year_month")
    .agg(
        revenue=("revenue", "sum"),
        profit=("gross_profit", "sum"),
        orders=("transaction_id", "count")
    )
    .reset_index()
)
monthly_trend["mom_growth_pct"] = np.round(monthly_trend["revenue"].pct_change() * 100, 2)

print("\n=== LAST 6 MONTHS SALES TREND ===")
print(monthly_trend.tail(6).to_string(index=False))

# 5. ABC-XYZ INVENTORY & PRODUCT SEGMENTATION
sku_monthly = df_clean.groupby(["sku", "year_month"])["revenue"].sum().unstack(fill_value=0)
abc_xyz = pd.DataFrame({
    "total_revenue": sku_monthly.sum(axis=1),
    "mean_monthly_rev": sku_monthly.mean(axis=1),
    "std_monthly_rev": sku_monthly.std(axis=1)
}).sort_values(by="total_revenue", ascending=False)

abc_xyz["cum_rev_pct"] = abc_xyz["total_revenue"].cumsum() / abc_xyz["total_revenue"].sum() * 100
abc_xyz["cv"] = abc_xyz["std_monthly_rev"] / (abc_xyz["mean_monthly_rev"] + 1e-9)
abc_xyz["ABC_class"] = pd.cut(abc_xyz["cum_rev_pct"], bins=[0, 80, 95, 100.1], labels=["A", "B", "C"])
abc_xyz["XYZ_class"] = pd.cut(abc_xyz["cv"], bins=[-1, 0.25, 0.50, np.inf], labels=["X", "Y", "Z"])
abc_xyz["segment"] = abc_xyz["ABC_class"].astype(str) + abc_xyz["XYZ_class"].astype(str)

print("\n=== ABC-XYZ SEGMENTATION DISTRIBUTION ===")
print(abc_xyz["segment"].value_counts())

# 6. HYPOTHESIS TESTING: PROMO VS NON-PROMO BASKET SIZE
promo_rev = df_clean[df_clean["is_promo"] == 1]["revenue"]
regular_rev = df_clean[df_clean["is_promo"] == 0]["revenue"]
t_stat, p_val = stats.ttest_ind(promo_rev, regular_rev, equal_var=False)

print(f"\n=== PROMO A/B STATISTICAL TEST ===")
print(f"Promo Mean Basket: {promo_rev.mean():.2f} AZN | Regular Mean Basket: {regular_rev.mean():.2f} AZN")
print(f"T-statistic: {t_stat:.4f}, P-value: {p_val:.6f}")
