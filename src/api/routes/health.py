import time
import sqlite3

from fastapi import APIRouter

from src.api.database import get_connection

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)

START_TIME = time.time()

@router.get("/")
def get_health():
    """Return the API health status and database statistics."""
    conn = get_connection()

    cursor = conn.cursor()
    tables = [

    "companies",

    "balancesheet",

    "cashflow",

    "profitandloss",

    "financial_ratios",

    "market_cap",

    "analysis",

    "documents",

    "peer_groups",

    "sectors"

]
    row_counts = {}

    for table in tables:

        cursor.execute(

        f"SELECT COUNT(*) FROM {table}"

    )

        row_counts[table] = cursor.fetchone()[0]

    conn.close()

    uptime = round(

    time.time() - START_TIME,

    2

)
    return {

    "status": "ok",

    "version": "1.0.0",

    "uptime_seconds": uptime,

    "db_row_counts": row_counts

}