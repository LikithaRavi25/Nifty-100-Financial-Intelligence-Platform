import sqlite3
import pandas as pd
from pathlib import Path

# ---------------------------------------------------
# Project Paths
# ---------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

# Change this if your database is in another folder
DB_PATH = BASE_DIR / "nifty100.db"

OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------
# Database Connection
# ---------------------------------------------------

conn = sqlite3.connect(DB_PATH)

# ---------------------------------------------------
# Latest Market Cap Data
# ---------------------------------------------------

market = pd.read_sql(
    """
    SELECT *
    FROM market_cap mc
    WHERE year = (
        SELECT MAX(year)
        FROM market_cap m2
        WHERE m2.company_id = mc.company_id
    )
    """,
    conn
)

# ---------------------------------------------------
# Latest Financial Ratios
# ---------------------------------------------------

ratios = pd.read_sql(
    """
    SELECT *
    FROM financial_ratios fr
    WHERE year = (
        SELECT MAX(year)
        FROM financial_ratios f2
        WHERE f2.company_id = fr.company_id
    )
    """,
    conn
)

sectors = pd.read_sql(
    """
    SELECT
        company_id,
        broad_sector
    FROM sectors
    """,
    conn
)



# ---------------------------------------------------
# Merge
# ---------------------------------------------------

valuation = ratios.merge(
    market,
    on="company_id",
    how="left",
    suffixes=("", "_market")
)
valuation = valuation.merge(
    sectors,
    on="company_id",
    how="left"
)

sector_pe = (
    valuation
    .groupby("broad_sector")["pe_ratio"]
    .median()
    .reset_index()
)

sector_pe.rename(
    columns={
        "pe_ratio":"sector_median_pe"
    },
    inplace=True
)

valuation = valuation.merge(
    sector_pe,
    on="broad_sector",
    how="left"
)
# ---------------------------------------------------
# Calculate FCF Yield
# ---------------------------------------------------

valuation["fcf_yield_pct"] = (
    valuation["free_cash_flow_cr"]
    / valuation["market_cap_crore"]
    * 100
).round(2)



# ---------------------------------------------------
# Verification
# ---------------------------------------------------

print("\nShape:")
print(valuation.shape)

print("\nColumns:")
print(valuation.columns.tolist())

print("\nSample:")
print(
    valuation[
        [
            "company_id",
            "free_cash_flow_cr",
            "market_cap_crore",
            "fcf_yield_pct"
        ]
    ].head()
)

print(
    valuation[
        ["company_id","broad_sector","pe_ratio"]
    ].head()
)

print(
    valuation[
        [
            "company_id",
            "broad_sector",
            "pe_ratio",
            "sector_median_pe"
        ]
    ].head()
)

valuation["pe_vs_sector_pct"] = (
    valuation["pe_ratio"]
    /
    valuation["sector_median_pe"]
    *100
).round(2)

def valuation_flag(row):

    if row["pe_ratio"] > row["sector_median_pe"] * 1.5:
        return "Caution"

    elif row["pe_ratio"] < row["sector_median_pe"] * 0.7:
        return "Discount"

    else:
        return "Fair"
    
valuation["flag"] = valuation.apply(
    valuation_flag,
    axis=1
)

print(
    valuation[
        [
            "company_id",
            "pe_ratio",
            "sector_median_pe",
            "pe_vs_sector_pct",
            "flag"
        ]
    ].head(10)
)

# ---------------------------------------------------
# Save
# ---------------------------------------------------

valuation.to_excel(
    OUTPUT_DIR / "valuation_summary.xlsx",
    index=False
)
flags = valuation[
    valuation["flag"] != "Fair"
]

flags.to_csv(
    OUTPUT_DIR / "valuation_flags.csv",
    index=False
)

print("✅ valuation_flags.csv saved")
print("\n✅ valuation_summary.xlsx saved successfully!")

# ---------------------------------------------------
# Close DB
# ---------------------------------------------------

conn.close()