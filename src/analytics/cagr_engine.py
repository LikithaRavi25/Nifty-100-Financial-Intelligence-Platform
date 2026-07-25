import sqlite3
import pandas as pd

from cagr import (
    revenue_cagr,
    pat_cagr,
    eps_cagr
)

conn = sqlite3.connect("nifty100.db")

pl = pd.read_sql(
    "SELECT * FROM profitandloss",
    conn
)

print(pl.head())

pl = pl.sort_values(
    [
        "company_id",
        "year"
    ]
)

pl["revenue_cagr_5yr"] = None
pl["pat_cagr_5yr"] = None
pl["eps_cagr_5yr"] = None

companies = pl["company_id"].unique()

for company in companies:

    temp = pl[
        pl["company_id"] == company
    ].copy()

    temp = temp.sort_values("year")

    for i in range(5, len(temp)):

        current = temp.index[i]

        previous = temp.index[i - 5]

        rev = revenue_cagr(
            pl.loc[previous, "sales"],
            pl.loc[current, "sales"],
            5
        )[0]

        pat = pat_cagr(
            pl.loc[previous, "net_profit"],
            pl.loc[current, "net_profit"],
            5
        )[0]

        eps = eps_cagr(
            pl.loc[previous, "eps"],
            pl.loc[current, "eps"],
            5
        )[0]

        pl.loc[current, "revenue_cagr_5yr"] = rev
        pl.loc[current, "pat_cagr_5yr"] = pat
        pl.loc[current, "eps_cagr_5yr"] = eps

print(

    pl[
        [
            "company_id",
            "year",
            "sales",
            "revenue_cagr_5yr",
            "pat_cagr_5yr",
            "eps_cagr_5yr"
        ]
    ].head(20)

)

pl.to_sql(

    "profitandloss",

    conn,

    if_exists="replace",

    index=False

)

conn.close()

print("5-Year CAGR calculated successfully.")