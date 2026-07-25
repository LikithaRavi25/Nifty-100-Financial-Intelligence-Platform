from fastapi import APIRouter, Query, HTTPException
from src.api.database import get_connection
import pandas as pd

router = APIRouter(
    prefix="/screener",
    tags=["Screener"]
)

@router.get("/")
def stock_screener(

    min_roe: float | None = Query(None),

    max_de: float | None = Query(None),

    min_fcf: float | None = Query(None),

    sector: str | None = Query(None),

    min_rev_cagr_5yr: float | None = Query(None),

    min_pat_cagr_5yr: float | None = Query(None),

    max_pe: float | None = Query(None)

):
    conn = get_connection()
    query = """

SELECT

c.id,

REPLACE(c.company_name,char(10),' ') AS company_name,

s.broad_sector,

s.market_cap_category,

r.return_on_equity_pct,

r.debt_to_equity,

r.free_cash_flow_cr,

m.pe_ratio,

a.compounded_sales_growth,
a.compounded_profit_growth

FROM companies c

LEFT JOIN sectors s
ON c.id=s.company_id

LEFT JOIN financial_ratios r
ON c.id=r.company_id

LEFT JOIN market_cap m
ON c.id=m.company_id

LEFT JOIN analysis a
ON c.id=a.company_id

WHERE

r.year=(

SELECT MAX(year)

FROM financial_ratios x

WHERE x.company_id=c.id

)

AND

m.year=(

SELECT MAX(year)

FROM market_cap x

WHERE x.company_id=c.id

)

"""
    filters = []

    params = []
    if min_roe is not None:

        filters.append(
        "r.return_on_equity_pct >= ?"
    )

        params.append(min_roe)

    if max_de is not None:

        filters.append(
        "r.debt_to_equity <= ?"
    )

        params.append(max_de)

    if min_fcf is not None:

        filters.append(
        "r.free_cash_flow_cr >= ?"
    )

        params.append(min_fcf)
    if sector:

        filters.append(
        "s.broad_sector=?"
    )

        params.append(sector)

    if min_rev_cagr_5yr is not None:

        filters.append(
        "CAST(REPLACE(a.compounded_sales_growth,'%','') AS REAL) >= ?"
    )

        params.append(min_rev_cagr_5yr)

    if min_pat_cagr_5yr is not None:

        filters.append(
        "CAST(REPLACE(a.compounded_profit_growth,'%','') AS REAL) >= ?"
    )

        params.append(min_pat_cagr_5yr)

    if max_pe is not None:

        filters.append(
        "m.pe_ratio<=?"
    )

        params.append(max_pe)

    if filters:

        query += " AND " + " AND ".join(filters)

    query += """

ORDER BY

r.return_on_equity_pct DESC

"""
    companies = pd.read_sql(

    query,

    conn,

    params=params

)

    conn.close()
    if min_roe is not None and min_roe < 0:

        raise HTTPException(

        status_code=400,

        detail="min_roe must be positive"

    )

    companies = companies.astype(object)
    companies = companies.where(pd.notna(companies), None)
    return companies.to_dict(
    orient="records"
)