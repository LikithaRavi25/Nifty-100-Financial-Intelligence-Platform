import sqlite3
import pandas as pd

from pathlib import Path
from cashflow_kpis import capital_allocation_pattern

BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "nifty100.db"

OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

conn = sqlite3.connect(DB_PATH)

query = """
SELECT

    c.company_name,

    fr.*,

    cf.operating_activity,
    cf.investing_activity,
    cf.financing_activity,
    cf.net_cash_flow

FROM financial_ratios fr

JOIN companies c
ON fr.company_id = c.id

LEFT JOIN cashflow cf
ON fr.company_id = cf.company_id
AND fr.year = cf.year

WHERE fr.year = (
    SELECT MAX(year)
    FROM financial_ratios f2
    WHERE f2.company_id = fr.company_id
)
"""

df = pd.read_sql(query, conn)

print(df.shape)

def classify_cashflow(row):

    cfo = row["cfo_quality_score"]
    fcf = row["free_cash_flow_cr"]

    if pd.isna(cfo) or pd.isna(fcf):
        return "Insufficient Data"

    if cfo >= 0.8 and fcf > 0:
        return "Excellent Cash Generator"

    elif cfo >= 0.6 and fcf > 0:
        return "Healthy Cash Flow"

    elif cfo >= 0.4:
        return "Moderate Cash Flow"

    else:
        return "Weak Cash Flow"
    
df["cashflow_classification"] = df.apply(
    classify_cashflow,
    axis=1
)

def confidence_score(row):

    cfo = row["cfo_quality_score"]

    if pd.isna(cfo):
        return 50

    if cfo >= 0.8:
        return 95

    elif cfo >= 0.6:
        return 85

    elif cfo >= 0.4:
        return 70

    else:
        return 55
    
def distress_signal(row):

    if (
        pd.isna(row["operating_activity"]) or
        pd.isna(row["financing_activity"])
    ):
        return "No"

    if (
        row["operating_activity"] < 0 and
        row["financing_activity"] > 0
    ):
        return "Yes"

    return "No"

def deleveraging_flag(row):

    if pd.isna(row["financing_activity"]):
        return "Unknown"

    if row["financing_activity"] < 0:
        return "Yes"

    return "No"
    
df["confidence_pct"] = df.apply(
    confidence_score,
    axis=1
)

df["distress_signal"] = df.apply(
    distress_signal,
    axis=1
)
df["capital_allocation"] = df.apply(

    lambda row: capital_allocation_pattern(

        row["operating_activity"],
        row["investing_activity"],
        row["financing_activity"],
        row["cfo_quality_score"]

    ),

    axis=1

)

df["deleveraging"] = df.apply(
    deleveraging_flag,
    axis=1
)
print(
    df[
        [
            "company_id",
            "company_name",
            "cfo_quality_score",
            "free_cash_flow_cr",
            "cashflow_classification",
            "confidence_pct"
        ]
    ].head(10)
)
summary = (
    df["cashflow_classification"]
    .value_counts()
)

print(summary)

output = df[
    [
        "company_id",
        "company_name",
        "cfo_quality_score",
        "free_cash_flow_cr",
        "cashflow_classification",
        "confidence_pct",
        "operating_activity",
        "investing_activity",
        "financing_activity",
        "capital_allocation",
        "distress_signal",
        "deleveraging"
    ]
]

output.to_csv(
    OUTPUT_DIR / "cashflow_intelligence.csv",
    index=False
)

output.to_excel(
    OUTPUT_DIR / "cashflow_intelligence.xlsx",
    index=False
)
distress = output[
    output["distress_signal"] == "Yes"
]

distress.to_csv(
    OUTPUT_DIR / "distress_alerts.csv",
    index=False
)

print("✅ distress_alerts.csv saved")

print("✅ cashflow_intelligence.csv saved")

print("\n=================================")
print("Cash Flow Intelligence Completed")
print("=================================\n")

print("Companies Analysed :", len(output))

print("\nClassification Summary")
print(summary)

print("\nAverage CFO Quality Score :",
      round(df["cfo_quality_score"].mean(), 2))

print("Average Free Cash Flow :",
      round(df["free_cash_flow_cr"].mean(), 2))

print("\nOutput File : cashflow_intelligence.csv")
print("\nCapital Allocation Summary")
print(df["capital_allocation"].value_counts())

print("\nDistress Signals :",
      (df["distress_signal"] == "Yes").sum())

print("Deleveraging Companies :",
      (df["deleveraging"] == "Yes").sum())

print(df.columns.tolist())


