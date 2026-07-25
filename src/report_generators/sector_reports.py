import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

conn = sqlite3.connect(BASE_DIR/"nifty100.db")

sector_df = pd.read_sql("""
SELECT
c.id,
c.company_name,
s.broad_sector,
s.sub_sector,
s.market_cap_category,
s.index_weight_pct
FROM companies c

JOIN sectors s
ON c.id = s.company_id

ORDER BY
s.broad_sector,
c.company_name
""", conn)

print(sector_df.head())

sectors = sorted(
    sector_df["broad_sector"].dropna().unique()
)

print(sectors)


SECTOR_DIR = (
    BASE_DIR /
    "output" /
    "reports" /
    "sector"
)

SECTOR_DIR.mkdir(
    parents=True,
    exist_ok=True
)

from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

styles = getSampleStyleSheet()

for sector in sectors:

    print(sector)

    companies = sector_df[
    sector_df["broad_sector"] == sector
]
    latest = pd.read_sql(f"""
    SELECT *

    FROM financial_ratios

    WHERE year=(
    SELECT MAX(year)
    FROM financial_ratios f2
    WHERE f2.company_id=financial_ratios.company_id
)
    """, conn)
    merged = companies.merge(
    latest,
    left_on="id",
    right_on="company_id"
)
    summary = pd.DataFrame({

    "Companies":[len(merged)],

    "Median ROE":[
        round(merged["return_on_equity_pct"].median(),2)
    ],

    "Median ROCE":[
        round(merged["return_on_capital_employed_pct"].median(),2)
    ],

    "Median Debt/Equity":[
        round(merged["debt_to_equity"].median(),2)
    ],

    "Median FCF":[
        round(merged["free_cash_flow_cr"].median(),2)
    ],

    "Average Index Weight":[
        round(merged["index_weight_pct"].mean(),2)
    ]

})

    print(summary)
    doc = SimpleDocTemplate(
    str(SECTOR_DIR/f"{sector}.pdf"),
    pagesize=A4
)

    story = []

    story.append(
    Paragraph(
        f"<b>{sector} Sector Report</b>",
        styles["Title"]
    )
)

    story.append(
    Spacer(1,20)
)
    table = Table(
    [summary.columns.tolist()]
    +
    summary.values.tolist()
)

    table.setStyle([
    ("GRID",(0,0),(-1,-1),1,"black"),
    ("BACKGROUND",(0,0),(-1,0),"lightgrey")
])

    story.append(table)

    story.append(Spacer(1,20))
    company_table = merged[[
    "company_name",
    "sub_sector",
    "market_cap_category",
    "return_on_equity_pct",
    "return_on_capital_employed_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "cfo_quality_score",
    "fcf_conversion_rate"
]]
    data = [
company_table.columns.tolist()
]

    data.extend(
company_table.values.tolist()
)

    t = Table(data)

    t.setStyle([
("GRID",(0,0),(-1,-1),0.5,"grey"),
("BACKGROUND",(0,0),(-1,0),"lightgrey"),
("FONTSIZE",(0,0),(-1,-1),7)
])

    story.append(t)

    doc.build(story)

    print(sector,"done")

import os

print(

len(

os.listdir(

BASE_DIR/
"output"/
"reports"

)

)

)