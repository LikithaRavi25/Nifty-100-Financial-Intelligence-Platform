from fastapi import APIRouter, HTTPException
from src.api.database import get_connection
import pandas as pd

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

@router.get("/{ticker}")
def get_documents(
    ticker: str
):
    conn = get_connection()
    query = """

SELECT *

FROM documents

WHERE company_id=?

ORDER BY year DESC

"""

    documents = pd.read_sql(

    query,

    conn,

    params=[ticker.upper()]

)

    conn.close()
    if documents.empty:

        raise HTTPException(

        status_code=404,

        detail="Documents not found"

    )
    return documents.to_dict(
    orient="records"
)