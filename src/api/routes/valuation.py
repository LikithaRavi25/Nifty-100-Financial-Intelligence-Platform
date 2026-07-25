from fastapi import APIRouter, HTTPException
from src.api.database import get_connection
import pandas as pd

router = APIRouter(
    prefix="/valuation",
    tags=["Valuation"]
)

@router.get("/{ticker}")
def get_valuation(ticker: str):

    conn = get_connection()

    query = """

    SELECT

    company_id,

    year,

    market_cap_crore,

    enterprise_value_crore,

    pe_ratio,

    pb_ratio,

    ev_ebitda,

    dividend_yield_pct

    FROM market_cap

    WHERE

    company_id=?

    AND

    year=(

        SELECT MAX(year)

        FROM market_cap m2

        WHERE m2.company_id=market_cap.company_id

    )

    """

    valuation = pd.read_sql(

        query,

        conn,

        params=[ticker.upper()]

    )

    conn.close()

    if valuation.empty:

        raise HTTPException(

            status_code=404,

            detail="Valuation data not found"

        )

    return valuation.iloc[0].to_dict()