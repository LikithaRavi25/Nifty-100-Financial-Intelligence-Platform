import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from pathlib import Path

from scipy.stats import zscore

BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "nifty100.db"

OUTPUT_DIR = BASE_DIR / "output"

REPORT_DIR = OUTPUT_DIR / "reports"

OUTPUT_DIR.mkdir(exist_ok=True)

REPORT_DIR.mkdir(exist_ok=True)

conn = sqlite3.connect(DB_PATH)

clusters = pd.read_csv(
    OUTPUT_DIR / "cluster_labels.csv"
)

print(clusters.shape)

print(clusters.head())

query = """

SELECT

company_id,

year,

return_on_equity_pct,

debt_to_equity,

sales,

free_cash_flow_cr,

operating_profit_margin_pct,

return_on_capital_employed_pct,

net_profit_margin_pct,

asset_turnover,

interest_coverage

FROM financial_ratios

WHERE year=(

SELECT MAX(year)

FROM financial_ratios f2

WHERE f2.company_id=
financial_ratios.company_id

)

"""

financials = pd.read_sql(query, conn)

print(financials.shape)

print(financials.head())

df = clusters.merge(
    financials,
    on="company_id",
    how="left"
)

print(df.shape)

print(df.head())

profile_columns = [

    "return_on_equity_pct",

    "debt_to_equity",

    "sales",

    "free_cash_flow_cr",

    "operating_profit_margin_pct"

]

cluster_mean = (

    df

    .groupby("cluster_id")[profile_columns]

    .mean()

    .round(2)

)

cluster_median = (

    df

    .groupby("cluster_id")[profile_columns]

    .median()

    .round(2)

)

print("\nCluster Mean Profile")

print(cluster_mean)

print("\nCluster Median Profile")

print(cluster_median)

cluster_mean.to_csv(

    OUTPUT_DIR /

    "cluster_profile_mean.csv"

)

cluster_median.to_csv(

    OUTPUT_DIR /

    "cluster_profile_median.csv"

)

print("✅ cluster_profile_mean.csv saved")

print("✅ cluster_profile_median.csv saved")

for cluster in sorted(df["cluster_id"].unique()):

    print("\n===================================")
    print(f"Cluster {cluster}")
    print("===================================")

    print(
        df[
            df["cluster_id"] == cluster
        ][
            [
                "company_id",
                "cluster_name",
                "return_on_equity_pct",
                "debt_to_equity"
            ]
        ].head(10)
    )

    cluster_mapping = {

    0: "High-Quality Compounders",

    1: "Emerging Growth",

    2: "Value Cyclicals",

    3: "Highly Leveraged",

    4: "Turnaround Candidates"

}
    
    df["cluster_name"] = (
    df["cluster_id"]
      .map(cluster_mapping)
)
    
    print(
    df[
        [
            "company_id",
            "cluster_id",
            "cluster_name"
        ]
    ].head(10)
)
    
    df[
    [
        "company_id",
        "cluster_id",
        "cluster_name",
        "distance_from_centroid"
    ]
].to_csv(

    OUTPUT_DIR /
    "cluster_labels.csv",

    index=False

)

print("✅ cluster_labels.csv updated")

kpi_columns = [

    "return_on_equity_pct",

    "return_on_capital_employed_pct",

    "net_profit_margin_pct",

    "operating_profit_margin_pct",

    "debt_to_equity",

    "sales",

    "free_cash_flow_cr",

    "asset_turnover",

    "interest_coverage",

    "distance_from_centroid"

]

correlation = df[kpi_columns].corr(
    method="pearson"
)

print(correlation)

plt.figure(figsize=(12,9))

sns.heatmap(

    correlation,

    annot=True,

    cmap="RdYlGn",

    center=0,

    linewidths=0.5,

    fmt=".2f"

)

plt.title(
    "Financial KPI Correlation Matrix"
)

plt.tight_layout()

plt.savefig(

    REPORT_DIR /

    "correlation_heatmap.png",

    dpi=300

)

plt.close()

print("✅ correlation_heatmap.png saved")

outlier_columns = [

    "return_on_equity_pct",

    "return_on_capital_employed_pct",

    "net_profit_margin_pct",

    "operating_profit_margin_pct",

    "debt_to_equity",

    "sales",

    "free_cash_flow_cr",

    "asset_turnover",

    "interest_coverage"

]
sector_df = pd.read_sql("""

SELECT

company_id,

broad_sector

FROM sectors

""", conn)

df = df.merge(

    sector_df,

    on="company_id",

    how="left"

)

df["broad_sector"] = df["broad_sector"].fillna("Unknown")

z_scores = (

    df

    .groupby("broad_sector")[outlier_columns]

    .transform(

        lambda x: zscore(x, nan_policy="omit")

    )

)

z_scores.columns = [

    column + "_zscore"

    for column in outlier_columns

]

df = pd.concat(

    [df, z_scores],

    axis=1

)

zscore_columns = z_scores.columns

df["is_outlier"] = (

    df[zscore_columns]

    .abs()

    .max(axis=1)

    > 3

)

outliers = df[

    df["is_outlier"]

]

print("\nOutliers Found :", len(outliers))

print(

    outliers[
        [
            "company_id",
            "broad_sector",
            "is_outlier"
        ]
    ]

)

outliers.to_csv(

    OUTPUT_DIR /

    "outlier_report.csv",

    index=False

)

print("✅ outlier_report.csv saved")

stats_columns = [

    "return_on_equity_pct",

    "return_on_capital_employed_pct",

    "net_profit_margin_pct",

    "operating_profit_margin_pct",

    "debt_to_equity",

    "sales",

    "free_cash_flow_cr",

    "asset_turnover",

    "interest_coverage"

]

portfolio_stats = []

for column in stats_columns:

    values = df[column].dropna()

portfolio_stats.append({

        "Metric": column,

        "P10": round(values.quantile(0.10), 2),

        "P25": round(values.quantile(0.25), 2),

        "P50": round(values.quantile(0.50), 2),

        "P75": round(values.quantile(0.75), 2),

        "P90": round(values.quantile(0.90), 2),

        "Mean": round(values.mean(), 2),

        "Std": round(values.std(), 2)

    })
portfolio_stats = pd.DataFrame(
portfolio_stats
)
print(portfolio_stats)
portfolio_stats.to_csv(

    OUTPUT_DIR /

    "portfolio_stats.csv",

    index=False

)

print("✅ portfolio_stats.csv saved")

print("\n====================================")
print("Cluster Profiling Completed")
print("====================================")

print("Companies Analysed :", len(df))

print("Clusters :", df["cluster_id"].nunique())

print("Outliers Found :", len(outliers))

print("\nGenerated Files")
print("--------------------------")
print("cluster_profile_mean.csv")
print("cluster_profile_median.csv")
print("correlation_heatmap.png")
print("outlier_report.csv")
print("portfolio_stats.csv")