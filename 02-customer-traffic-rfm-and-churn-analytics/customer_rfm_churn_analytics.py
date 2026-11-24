"""
================================================================================
PROJECT 02: CUSTOMER DATABASE ANALYTICS, RFM & CHURN PREDICTION
Author: Aysu Gadirova | Senior Data Analyst
Domain: Customer Foot-Traffic Growth, Retention & Behavioral Segmentation
Tech Stack: Python (Pandas, NumPy, Scikit-Learn), SQL
================================================================================
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score

# 1. SIMULATED CUSTOMER & VISIT / TRANSACTION DATABASE
np.random.seed(101)
n_customers = 3000

customers = pd.DataFrame({
    "customer_id": [f"CUST-{20000 + i}" for i in range(n_customers)],
    "signup_date": pd.to_datetime("2023-01-01") + pd.to_timedelta(
        np.random.randint(0, 900, size=n_customers), unit="D"
    ),
    "age": np.random.randint(18, 58, size=n_customers),
    "city_district": np.random.choice(["Sabail", "Nasimi", "Narimanov", "Khatai", "Yasamal"], size=n_customers),
    "acquisition_channel": np.random.choice(["Instagram_Ads", "Walk_In", "Referral", "Loyalty_App"], size=n_customers)
})

n_visits = 22000
visits = pd.DataFrame({
    "visit_id": [f"VST-{500000 + i}" for i in range(n_visits)],
    "customer_id": np.random.choice(customers["customer_id"], size=n_visits),
    "visit_date": pd.to_datetime("2024-01-01") + pd.to_timedelta(
        np.random.randint(0, 700, size=n_visits), unit="D"
    ),
    "spend_azn": np.round(np.random.gamma(shape=3.0, scale=18.0, size=n_visits), 2),
    "satisfaction_score": np.random.choice([1, 2, 3, 4, 5], size=n_visits, p=[0.04, 0.06, 0.15, 0.35, 0.40])
})

visits = visits.merge(customers[["customer_id", "signup_date"]], on="customer_id", how="left")
visits = visits[visits["visit_date"] >= visits["signup_date"]].copy()

# 2. RFM (RECENCY, FREQUENCY, MONETARY) CUSTOMER SEGMENTATION
snapshot_date = visits["visit_date"].max() + pd.Timedelta(days=1)

rfm = (
    visits.groupby("customer_id")
    .agg(
        recency=("visit_date", lambda x: (snapshot_date - x.max()).days),
        frequency=("visit_id", "count"),
        monetary=("spend_azn", "sum"),
        avg_satisfaction=("satisfaction_score", "mean")
    )
    .reset_index()
)

rfm["R_score"] = pd.qcut(rfm["recency"], q=4, labels=[4, 3, 2, 1]).astype(int)
rfm["F_score"] = pd.qcut(rfm["frequency"].rank(method="first"), q=4, labels=[1, 2, 3, 4]).astype(int)
rfm["M_score"] = pd.qcut(rfm["monetary"], q=4, labels=[1, 2, 3, 4]).astype(int)
rfm["RFM_total"] = rfm["R_score"] + rfm["F_score"] + rfm["M_score"]

def assign_rfm_segment(row):
    if row["R_score"] >= 3 and row["F_score"] >= 3 and row["M_score"] >= 3:
        return "Champions"
    elif row["F_score"] >= 3 and row["R_score"] >= 2:
        return "Loyal_Customers"
    elif row["R_score"] <= 2 and row["F_score"] >= 3:
        return "At_Risk_High_Value"
    elif row["R_score"] == 1:
        return "Hibernating_Churned"
    else:
        return "Potential_Loyalists"

rfm["segment"] = rfm.apply(assign_rfm_segment, axis=1)

print("=== RFM CUSTOMER SEGMENTATION SUMMARY ===")
print(
    rfm.groupby("segment")
    .agg(
        customers=("customer_id", "count"),
        avg_recency_days=("recency", "mean"),
        avg_frequency=("frequency", "mean"),
        avg_monetary_azn=("monetary", "mean")
    )
    .round(2)
)

# 3. COHORT RETENTION ANALYSIS
visits["visit_month"] = visits["visit_date"].dt.to_period("M")
visits["cohort_month"] = visits.groupby("customer_id")["visit_date"].transform("min").dt.to_period("M")
visits["cohort_index"] = (visits["visit_month"] - visits["cohort_month"]).apply(lambda x: x.n)

cohort_data = visits.groupby(["cohort_month", "cohort_index"])["customer_id"].nunique().reset_index()
cohort_pivot = cohort_data.pivot(index="cohort_month", columns="cohort_index", values="customer_id")
retention_matrix = np.round(cohort_pivot.divide(cohort_pivot.iloc[:, 0], axis=0) * 100, 1)

print("\n=== COHORT RETENTION MATRIX (% - LAST 6 COHORTS) ===")
print(retention_matrix.iloc[-6:, :6])

# 4. PREDICTIVE CHURN MODELING
model_df = customers.merge(rfm, on="customer_id", how="inner")
model_df["is_churned"] = (model_df["recency"] > 90).astype(int)

features = ["age", "frequency", "monetary", "avg_satisfaction"]
X = pd.get_dummies(model_df[features + ["acquisition_channel"]], drop_first=True)
y = model_df["is_churned"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

rf_clf = RandomForestClassifier(n_estimators=150, max_depth=8, random_state=42)
rf_clf.fit(X_train, y_train)
y_pred = rf_clf.predict(X_test)
y_prob = rf_clf.predict_proba(X_test)[:, 1]

print(f"\n=== CHURN PREDICTION MODEL (ROC-AUC: {roc_auc_score(y_test, y_prob):.4f}) ===")
print(classification_report(y_test, y_pred))
