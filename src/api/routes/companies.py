from fastapi import APIRouter, Query, HTTPException
from src.api.database import get_connection
import pandas as pd
from fastapi.responses import FileResponse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]

REPORTS_DIR = (
    BASE_DIR /
    "output" /
    "reports"
)

router = APIRouter(
    prefix="/companies",
    tags=["Companies"]
)

@router.get("/")
def get_companies(

    sector: str | None = Query(None),

    market_cap_category: str | None = Query(None),

    search: str | None = Query(None)

):
    conn = get_connection()
    query = """

SELECT

c.id,

REPLACE(c.company_name, char(10), ' ') AS company_name,

s.broad_sector,

s.sub_sector,

s.market_cap_category,

f.return_on_equity_pct,

f.return_on_capital_employed_pct

FROM companies c

LEFT JOIN sectors s

ON c.id=s.company_id

LEFT JOIN financial_ratios f

ON c.id=f.company_id

WHERE f.year=(

SELECT MAX(year)

FROM financial_ratios x

WHERE x.company_id=c.id

)

"""

    filters = []

    params = []

    if sector:

        filters.append(
        "s.broad_sector = ?"
    )
        params.append(sector)

    if market_cap_category:

        filters.append(
        "s.market_cap_category = ?"
    )

        params.append(
        market_cap_category
    )
    if search:

        filters.append(

        "(c.company_name LIKE ? OR c.id LIKE ?)"

    )

        params.append(f"%{search}%")

        params.append(f"%{search}%")

    if filters:

        query += " AND " + " AND ".join(filters)

    query += " ORDER BY c.company_name"

    companies = pd.read_sql(
    query,
    conn,
    params=params
)

    conn.close()
    print(companies.dtypes)
    print(companies.head())
    import json

    return json.loads(
    companies.to_json(
        orient="records"
    )
)

@router.get("/{ticker}")
def get_company_profile(
    ticker: str
):
    conn = get_connection()
    query = """

SELECT

c.*,

s.broad_sector,

s.sub_sector,

s.market_cap_category,

f.return_on_equity_pct,

f.return_on_capital_employed_pct,

f.net_profit_margin_pct,

f.operating_profit_margin_pct,

f.debt_to_equity,

f.asset_turnover,

f.interest_coverage,

f.free_cash_flow_cr

FROM companies c

LEFT JOIN sectors s

ON c.id=s.company_id

LEFT JOIN financial_ratios f

ON c.id=f.company_id

WHERE

c.id=?

AND

f.year=(

SELECT MAX(year)

FROM financial_ratios x

WHERE x.company_id=c.id

)

"""

    company = pd.read_sql(
    query,
    conn,
    params=[ticker.upper()]
)

    conn.close()
    if company.empty:

        raise HTTPException(

        status_code=404,

        detail="Company not found"

    )
    company["company_name"] = (
    company["company_name"]
    .str.replace("\n", " ", regex=False)
)

    company = company.astype(object)
    company = company.where(pd.notna(company), None)

    return company.iloc[0].to_dict()

@router.get("/{ticker}/pl")
def get_profit_loss(

    ticker: str,

    from_year: str | None = Query(None),

    to_year: str | None = Query(None)

):
    conn = get_connection()
    query = """

SELECT *

FROM profitandloss

WHERE company_id=?

"""
    params = [ticker.upper()]
    if from_year:

        query += " AND year >= ?"

        params.append(from_year)

    if to_year:

        query += " AND year <= ?"

        params.append(to_year)

    query += """

ORDER BY year

"""

    pl = pd.read_sql(

    query,

    conn,

    params=params

)

    conn.close()
    if pl.empty:

        raise HTTPException(

        status_code=404,

        detail="Profit & Loss data not found"

    )

    pl = pl.astype(object)
    pl = pl.where(pd.notna(pl), None)

    return pl.to_dict(
    orient="records"
)


@router.get("/{ticker}/bs")
def get_balance_sheet(

    ticker: str,

    from_year: str | None = Query(None),

    to_year: str | None = Query(None)

):
    conn = get_connection()
    query = """

SELECT *

FROM balancesheet

WHERE company_id=?

"""
    params = [ticker.upper()]

    if from_year:

       query += " AND year >= ?"

       params.append(from_year)

    if to_year:

       query += " AND year <= ?"

       params.append(to_year)

    query += " ORDER BY year"

    bs = pd.read_sql(

    query,

    conn,

    params=params

)

    conn.close()
    if bs.empty:

        raise HTTPException(

        status_code=404,

        detail="Balance Sheet data not found"

    )
    bs = bs.astype(object)
    bs = bs.where(pd.notna(bs), None)

    return bs.to_dict(
    orient="records"
)

@router.get("/{ticker}/cashflow")
def get_cashflow(

    ticker: str,

    from_year: str | None = Query(None),

    to_year: str | None = Query(None)

):

    conn = get_connection()

    query = """

    SELECT *

    FROM cashflow

    WHERE company_id=?

    """

    params = [ticker.upper()]

    if from_year:

        query += " AND year >= ?"

        params.append(from_year)

    if to_year:

        query += " AND year <= ?"

        params.append(to_year)

    query += " ORDER BY year"

    cashflow = pd.read_sql(

        query,

        conn,

        params=params

    )

    conn.close()

    if cashflow.empty:

        raise HTTPException(

            status_code=404,

            detail="Cash Flow data not found"

        )

    cashflow = cashflow.astype(object)
    cashflow = cashflow.where(pd.notna(cashflow), None)

    return cashflow.to_dict(
    orient="records"
)


@router.get("/{ticker}/ratios")
def get_financial_ratios(

    ticker: str,

    year: str | None = Query(None)

):

    conn = get_connection()

    query = """

    SELECT *

    FROM financial_ratios

    WHERE company_id=?

    """

    params = [ticker.upper()]

    if year:

        query += " AND year=?"

        params.append(year)

    query += " ORDER BY year DESC"

    ratios = pd.read_sql(

        query,

        conn,

        params=params

    )

    conn.close()

    if ratios.empty:

        raise HTTPException(

            status_code=404,

            detail="Financial Ratios not found"

        )

    ratios = ratios.astype(object)
    ratios = ratios.where(pd.notna(ratios), None)

    return ratios.to_dict(
    orient="records"
)


@router.get("/{ticker}/tearsheet")
def download_tearsheet(

    ticker: str

):

    pdf_path = REPORTS_DIR / f"{ticker.upper()}.pdf"

    if not pdf_path.exists():

        raise HTTPException(

            status_code=404,

            detail="Tearsheet not found"

        )

    return FileResponse(

        path=pdf_path,

        media_type="application/pdf",

        filename=f"{ticker.upper()}.pdf"

    )

