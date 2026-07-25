from fastapi import APIRouter, HTTPException
from src.api.database import get_connection
import pandas as pd

router = APIRouter(
    prefix="/sectors",
    tags=["Sectors"]
)

@router.get("/")
def get_sectors():

    conn = get_connection()

    query = """

    SELECT

    s.broad_sector,

    COUNT(DISTINCT s.company_id) AS company_count,

    AVG(r.return_on_equity_pct) AS avg_roe,

    AVG(m.pe_ratio) AS avg_pe,

    AVG(r.debt_to_equity) AS avg_de

    FROM sectors s

    LEFT JOIN financial_ratios r
    ON s.company_id = r.company_id

    LEFT JOIN market_cap m
    ON s.company_id = m.company_id

    WHERE

    r.year = (
        SELECT MAX(year)
        FROM financial_ratios x
        WHERE x.company_id = s.company_id
    )

    AND

    m.year = (
        SELECT MAX(year)
        FROM market_cap x
        WHERE x.company_id = s.company_id
    )

    GROUP BY s.broad_sector

    ORDER BY s.broad_sector

    """

    sector_df = pd.read_sql(
        query,
        conn
    )

    conn.close()
    sector_df = sector_df.astype(object)
    sector_df = sector_df.where(pd.notna(sector_df), None)


    return sector_df.to_dict(
        orient="records"
    )

@router.get("/{sector}/companies")
def get_sector_companies(sector: str):

    conn = get_connection()

    query = """

    SELECT

    c.id,

    REPLACE(c.company_name,char(10),' ') AS company_name,

    s.sub_sector,
    s.broad_sector,


    r.return_on_equity_pct,

    r.return_on_capital_employed_pct,

    r.debt_to_equity,

    r.free_cash_flow_cr,

    m.pe_ratio

    FROM companies c

    JOIN sectors s
    ON c.id=s.company_id

    LEFT JOIN financial_ratios r
    ON c.id=r.company_id

    LEFT JOIN market_cap m
    ON c.id=m.company_id

    WHERE

    s.broad_sector=?

    AND

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

    ORDER BY c.company_name

    """

    companies = pd.read_sql(

        query,

        conn,

        params=[sector]

    )

    conn.close()

    if companies.empty:

        raise HTTPException(

            status_code=404,

            detail="Sector not found"

        )
    companies = companies.astype(object)
    companies = companies.where(pd.notna(companies), None)


    return companies.to_dict(
        orient="records"
    )