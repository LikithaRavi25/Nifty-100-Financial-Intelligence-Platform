import sqlite3
import pandas as pd
from cashflow_kpis import capital_allocation_pattern

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "nifty100.db"

OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

conn = sqlite3.connect(DB_PATH)

query = """
SELECT

c.company_name,

cf.*

FROM cashflow cf

JOIN companies c

ON cf.company_id = c.id
"""

cashflow = pd.read_sql(query, conn)

print(cashflow.head())

print(cashflow.shape)

ratio_query = """
SELECT

company_id,
year,
cfo_quality_score

FROM financial_ratios
"""

ratios = pd.read_sql(
    ratio_query,
    conn
)

cashflow = cashflow.merge(

    ratios,

    on=[
        "company_id",
        "year"
    ],

    how="left"

)

print(cashflow.columns.tolist())

cashflow["capital_allocation"] = cashflow.apply(

    lambda row:

    capital_allocation_pattern(

        row["operating_activity"],

        row["investing_activity"],

        row["financing_activity"],

        row["cfo_quality_score"]

    ),

    axis=1

)

print(

cashflow[

[
"company_id",
"year",
"capital_allocation"

]

].head(20)

)

capital = pd.read_csv(
    OUTPUT_DIR / "capital_allocation.csv"
)

print(capital.head())
print(capital.shape)

print(
    "Companies :",
    capital["company_id"].nunique()
)

print(
    "Years :",
    capital["year"].nunique()
)
print(
    capital.isnull().sum()
)

cashflow["year_dt"] = pd.to_datetime(cashflow["year"])

latest = (
    cashflow
    .sort_values("year_dt")
    .drop_duplicates(
        subset="company_id",
        keep="last"
    )
)
print(latest)

distribution = (
    latest["capital_allocation"]
    .value_counts()
)

print(distribution)

distribution_df = (
    distribution
    .reset_index()
)

distribution_df.columns = [
    "Capital Allocation Pattern",
    "Company Count"
]

distribution_df.to_csv(

    OUTPUT_DIR /
    "capital_allocation_distribution.csv",

    index=False

)

print(
    "✅ capital_allocation_distribution.csv saved"
)

cashflow_report = pd.read_csv(
    OUTPUT_DIR / "cashflow_intelligence.csv"
)

latest_allocation = latest[
    [
        "company_id",
        "capital_allocation"
    ]
]

cashflow_report = cashflow_report.merge(
    latest_allocation,
    on="company_id",
    how="left"
)

cashflow_report.to_excel(
    OUTPUT_DIR / "cashflow_intelligence.xlsx",
    index=False
)

print("✅ cashflow_intelligence.xlsx updated")

cashflow = cashflow.sort_values(
    ["company_id", "year"]
)

cashflow["previous_pattern"] = (
    cashflow
    .groupby("company_id")["capital_allocation"]
    .shift(1)
)

pattern_changes = cashflow[
    (
        cashflow["previous_pattern"].notna()
    ) &
    (
        cashflow["capital_allocation"] !=
        cashflow["previous_pattern"]
    )
]

pattern_changes = pattern_changes[
    [
        "company_id",
        "company_name",
        "year",
        "previous_pattern",
        "capital_allocation"
    ]
]

pattern_changes.to_csv(
    OUTPUT_DIR / "pattern_changes.csv",
    index=False
)

print("✅ pattern_changes.csv saved")

print("\n=================================")
print("Capital Allocation Report Complete")
print("=================================\n")

print("Companies Analysed :", latest["company_id"].nunique())
print("Pattern Changes :", len(pattern_changes))

print("\nLatest Distribution")
print(distribution)

print("\nOutputs Generated")
print("- capital_allocation_distribution.csv")
print("- pattern_changes.csv")
print("- cashflow_intelligence.xlsx")

