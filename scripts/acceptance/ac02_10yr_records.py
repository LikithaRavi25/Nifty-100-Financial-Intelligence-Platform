import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")   # Change path if needed

query = """
SELECT
    c.id,

    COUNT(DISTINCT pl.year) AS pl_years,
    COUNT(DISTINCT bs.year) AS bs_years,
    COUNT(DISTINCT cf.year) AS cf_years

FROM companies c

LEFT JOIN profitandloss pl
ON c.id = pl.company_id

LEFT JOIN balancesheet bs
ON c.id = bs.company_id

LEFT JOIN cashflow cf
ON c.id = cf.company_id

GROUP BY c.id
"""

df = pd.read_sql(query, conn)

conn.close()

qualified = df[
    (df["pl_years"] >= 10) &
    (df["bs_years"] >= 10) &
    (df["cf_years"] >= 10)
]

print(df.head())

print("\nCompanies meeting requirement:", len(qualified))
print("Total companies:", len(df))

percentage = len(qualified) / len(df) * 100

print(f"Percentage: {percentage:.2f}%")

if percentage >= 90:
    print("\n✅ AC-02 PASS")
else:
    print("\n❌ AC-02 FAIL")

if percentage < 90:
    print("\nCompanies failing:")
    print(
        df[
            ~df.index.isin(qualified.index)
        ][["id","pl_years","bs_years","cf_years"]]
    )