from fastapi import APIRouter
from src.api.database import get_connection
import pandas as pd

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]

OUTPUT_DIR = BASE_DIR / "output"

router = APIRouter(
    prefix="/portfolio",
    tags=["Portfolio"]
)

@router.get("/")
def portfolio_summary():

    conn = get_connection()

    summary_query = """

    SELECT

    COUNT(DISTINCT company_id) AS total_companies,

    ROUND(AVG(return_on_equity_pct),2) AS avg_roe,

    ROUND(AVG(debt_to_equity),2) AS avg_de,

    ROUND(AVG(free_cash_flow_cr),2) AS avg_fcf

    FROM financial_ratios

    WHERE year=(

        SELECT MAX(year)

        FROM financial_ratios x

        WHERE x.company_id=financial_ratios.company_id

    )

    """

    summary = pd.read_sql(
        summary_query,
        conn
    ).iloc[0].to_dict()

    sector_query = """

    SELECT

    broad_sector,

    COUNT(*) AS company_count

    FROM sectors

    GROUP BY broad_sector

    ORDER BY company_count DESC

    """

    sector_allocation = pd.read_sql(
        sector_query,
        conn
    )

    cluster_df = pd.read_csv(
        OUTPUT_DIR / "cluster_labels.csv"
    )

    cluster_allocation = (

        cluster_df

        .groupby("cluster_name")

        .size()

        .reset_index(name="company_count")

    )

    conn.close()

    return {

        "summary": summary,

        "sector_allocation": sector_allocation.to_dict(
            orient="records"
        ),

        "cluster_allocation": cluster_allocation.to_dict(
            orient="records"
        )

    }