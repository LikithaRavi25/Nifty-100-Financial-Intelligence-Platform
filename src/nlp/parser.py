import re
import pandas as pd
from pathlib import Path
import sqlite3


BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "nifty100.db"

OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

conn = sqlite3.connect(DB_PATH)

analysis = pd.read_sql(
    """
    SELECT *
    FROM analysis
    """,
    conn
)

print(analysis.head())
print(analysis.columns)

pattern = r"(TTM|Last Year|\d+\s+Years?|\d+\s+Year)\s*:?\s*(-?\d+(?:\.\d+)?)%"

def parse_metric(text):

    if pd.isna(text):
        return None

    text = str(text).strip()

    match = re.search(pattern, text)

    if match:

        period = match.group(1)
        value = float(match.group(2))

        return period, value

    return None

samples = [

    "10 Years: 21%",
    "5 Years:       24%",
    "TTM:            43%",
    "Last Year:      12%",
    "1 Year: -2%"

]

for s in samples:

    print(s)

    print(parse_metric(s))

metric_columns = [

    "compounded_sales_growth",
    "compounded_profit_growth",
    "stock_price_cagr",
    "roe"

]
parsed_rows = []

failed_rows = []

for _, row in analysis.iterrows():

    company = row["company_id"]

    for metric in metric_columns:

        result = parse_metric(row[metric])

        if result:

            period, value = result

            parsed_rows.append({

                "company_id": company,
                "metric_type": metric,
                "period": period,
                "value_pct": value

            })

        else:

            failed_rows.append({

                "company_id": company,
                "metric": metric,
                "raw_text": row[metric]

            })

parsed = pd.DataFrame(parsed_rows)

failures = pd.DataFrame(failed_rows)
print(parsed.head())

print()

print(parsed.shape)

print()

print(failures.shape)

def normalize_period(period):

    if period == "TTM":
        return 0

    if period == "Last Year":
        return 1

    match = re.search(r"\d+", period)

    if match:
        return int(match.group())

    return None

parsed["period_years"] = parsed["period"].apply(normalize_period)
parsed = parsed[
    [
        "company_id",
        "metric_type",
        "period_years",
        "value_pct"
    ]
]
print(parsed.head())
parsed.to_csv(
    OUTPUT_DIR / "analysis_parsed.csv",
    index=False
)

print("✅ analysis_parsed.csv saved")
failures.to_csv(
    OUTPUT_DIR / "parse_failures.csv",
    index=False
)

print("✅ parse_failures.csv saved")

query = """
SELECT
    company_id,
    revenue_cagr_5yr,
    pat_cagr_5yr
FROM financial_ratios
WHERE year = (
    SELECT MAX(year)
    FROM financial_ratios f2
    WHERE f2.company_id = financial_ratios.company_id
)
"""

ratios = pd.read_sql(query, conn)
print(ratios.head())

validation = parsed[
    parsed["metric_type"].isin([
        "compounded_sales_growth",
        "compounded_profit_growth"
    ])
].copy()

validation["computed_value"] = None

for i, row in validation.iterrows():

    company = row["company_id"]

    metric = row["metric_type"]

    ratio = ratios[
        ratios["company_id"] == company
    ]

    if ratio.empty:
        continue

    if metric == "compounded_sales_growth":

        validation.loc[i, "computed_value"] = \
            ratio.iloc[0]["revenue_cagr_5yr"]

    elif metric == "compounded_profit_growth":

        validation.loc[i, "computed_value"] = \
            ratio.iloc[0]["pat_cagr_5yr"]
        
validation["difference_pct"] = (
    validation["value_pct"] -
    validation["computed_value"]
).abs()

validation["manual_review"] = validation[
    "difference_pct"
] > 5

validation.to_csv(
    OUTPUT_DIR / "cagr_validation.csv",
    index=False
)

print("✅ cagr_validation.csv saved")

print()

print("Companies Checked :", len(validation))

print(
    "Manual Review Required :",
    validation["manual_review"].sum()
)