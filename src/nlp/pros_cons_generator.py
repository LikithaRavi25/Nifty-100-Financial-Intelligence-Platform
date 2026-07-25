import sqlite3
import pandas as pd

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "nifty100.db"

OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

conn = sqlite3.connect(DB_PATH)

query = """
SELECT

c.company_name,

fr.*

FROM financial_ratios fr

JOIN companies c

ON fr.company_id=c.id

WHERE fr.year=
(
SELECT MAX(year)

FROM financial_ratios f2

WHERE f2.company_id=fr.company_id
)
"""
df = pd.read_sql(query, conn)

print(df.head())
records = []

def add_record(
        company_id,
        company_name,
        rtype,
        rule,
        text,
        confidence
):

    records.append({

        "company_id":company_id,

        "company_name":company_name,

        "type":rtype,

        "rule_id":rule,

        "text":text,

        "confidence_pct":confidence

    })

for _, row in df.iterrows():

    company=row["company_name"]

    cid=row["company_id"]

    if row["return_on_equity_pct"] >= 20:

        add_record(

        cid,
        company,

        "Pro",

        "P1",

        "Consistently high return on equity above 20% demonstrates exceptional capital efficiency.",

        95

    )
        
    if row["free_cash_flow_cr"] > 0:

        add_record(

        cid,

        company,

        "Pro",

        "P2",

        "Strong free cash flow generation signals healthy business fundamentals.",

        90

    )
        
    if row["debt_to_equity"]==0:

        add_record(

        cid,

        company,

        "Pro",

        "P3",

        "Debt-free balance sheet provides financial flexibility and eliminates interest burden.",

        95

    )
        
    if row["revenue_cagr_5yr"]>=15:

        add_record(

        cid,

        company,

        "Pro",

        "P4",

        "Revenue growing above 15% CAGR reflects strong business momentum.",

        90

    )
        
    if row["operating_profit_margin_pct"]>=25:

        add_record(

        cid,

        company,

        "Pro",

        "P5",

        "Operating margins above 25% indicate strong pricing power and cost discipline.",

        92

    )
        
    if row["pat_cagr_5yr"]>=20:

        add_record(

        cid,

        company,

        "Pro",

        "P6",

        "Net profit compounding above 20% creates significant shareholder value.",

        91

    )
    if (
    row["interest_coverage"] >= 10
    or row["debt_to_equity"] == 0
):

        add_record(
        cid,
        company,
        "Pro",
        "P7",
        "Very high interest coverage reflects negligible financial stress from debt servicing.",
        88
    )
    if (
    pd.notna(row["revenue_cagr_5yr"])
    and pd.notna(row["pat_cagr_5yr"])
    and row["pat_cagr_5yr"] > row["revenue_cagr_5yr"]
):

        add_record(
        cid,
        company,
        "Pro",
        "P11",
        "Profit growth outpacing revenue suggests improving operating leverage.",
        84
    )
        
    if (
    pd.notna(row["debt_to_equity"])
    and row["debt_to_equity"] > 2
):

        add_record(
        cid,
        company,
        "Con",
        "C1",
        f"Debt-to-equity ratio of {row['debt_to_equity']:.2f} indicates elevated financial leverage.",
        95
    )
        
    if (
    pd.notna(row["free_cash_flow_cr"])
    and row["free_cash_flow_cr"] < 0
):

        add_record(
        cid,
        company,
        "Con",
        "C2",
        "Negative free cash flow raises concerns about cash generation quality.",
        90
    )
    if (
    pd.notna(row["operating_profit_margin_pct"])
    and row["operating_profit_margin_pct"] < 10
):

        add_record(
        cid,
        company,
        "Con",
        "C3",
        "Operating profit margin is relatively low, indicating pricing or cost pressure.",
        84
    )
    if (
    pd.notna(row["net_profit_margin_pct"])
    and row["net_profit_margin_pct"] < 0
):

        add_record(
        cid,
        company,
        "Con",
        "C4",
        "Company reported a negative net profit margin in the latest financial year.",
        95
    )
    if (
    pd.notna(row["revenue_cagr_5yr"])
    and row["revenue_cagr_5yr"] < 5
):

        add_record(
        cid,
        company,
        "Con",
        "C5",
        "Revenue growth below 5% CAGR indicates weak business momentum.",
        85
    )
    if (
    pd.notna(row["interest_coverage"])
    and row["interest_coverage"] < 1.5
):

        add_record(
        cid,
        company,
        "Con",
        "C6",
        "Low interest coverage indicates difficulty servicing debt obligations.",
        95
    )
    if (
    pd.notna(row["dividend_payout"])
    and row["dividend_payout"] > 100
):

        add_record(
        cid,
        company,
        "Con",
        "C7",
        "Dividend payout above 100% may not be sustainable over the long term.",
        88
    )
    if (
    pd.notna(row["debt_to_equity"])
    and row["debt_to_equity"] > 4
):

        add_record(
        cid,
        company,
        "Con",
        "C8",
        "Very high debt levels significantly increase financial leverage risk.",
        96
    )
        
    if (
    pd.notna(row["return_on_capital_employed_pct"])
    and row["return_on_capital_employed_pct"] < 10
):

        add_record(
        cid,
        company,
        "Con",
        "C10",
        "Return on capital employed below 10% indicates weak capital efficiency.",
        90
    )
        
    if (
    pd.notna(row["cfo_quality_score"])
    and row["cfo_quality_score"] < 0.5
):

        add_record(
        cid,
        company,
        "Con",
        "C11",
        "Weak cash flow quality suggests lower earnings reliability.",
        87
    )
        
    if (
    pd.notna(row["pat_cagr_5yr"])
    and row["pat_cagr_5yr"] < 5
):

        add_record(
        cid,
        company,
        "Con",
        "C12",
        "Profit growth below 5% CAGR indicates limited earnings momentum.",
        84
    )

print("Total records:", len(records))
pros_cons = pd.DataFrame(records)

print(pros_cons.head())
pros_cons = pros_cons[
    pros_cons["confidence_pct"] >= 60
]
pros = (
    pros_cons[pros_cons["type"]=="Pro"]
    .groupby("company_id")
    .size()
)
cons = (
    pros_cons[pros_cons["type"]=="Con"]
    .groupby("company_id")
    .size()
)
missing_pro = set(df["company_id"]) - set(pros.index)
missing_con = set(df["company_id"]) - set(cons.index)
print("Companies without Pro :", len(missing_pro))
print("Companies without Con :", len(missing_con))

for cid in missing_pro:

    company = df.loc[
        df["company_id"]==cid,
        "company_name"
    ].iloc[0]

    records.append({

        "company_id":cid,

        "company_name":company,

        "type":"Pro",

        "rule_id":"DEFAULT",

        "text":"Stable business with no major positive financial signals identified.",

        "confidence_pct":65

    })

for cid in missing_con:

    company = df.loc[
        df["company_id"]==cid,
        "company_name"
    ].iloc[0]

    records.append({

        "company_id":cid,

        "company_name":company,

        "type":"Con",

        "rule_id":"DEFAULT",

        "text":"No major financial weaknesses detected, continued monitoring recommended.",

        "confidence_pct":65

    })

pros_cons = pd.DataFrame(records)
pros_cons = pros_cons.sort_values(

    ["company_name","type"]

).reset_index(drop=True)
pros_cons.to_csv(

    OUTPUT_DIR / "pros_cons_generated.csv",

    index=False

)

print()

print("====================================")

print("Pros & Cons Generation Completed")

print("====================================")

print()

print("Companies :", pros_cons["company_id"].nunique())

print("Total Statements :", len(pros_cons))

print("Pros :", len(pros_cons[pros_cons["type"]=="Pro"]))

print("Cons :", len(pros_cons[pros_cons["type"]=="Con"]))

print()

print("pros_cons_generated.csv saved")