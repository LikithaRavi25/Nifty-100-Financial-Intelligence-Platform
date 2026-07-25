from fastapi import APIRouter, HTTPException
from src.api.database import get_connection
import pandas as pd

router = APIRouter(
    prefix="/peers",
    tags=["Peers"]
)

@router.get("/{group_name}")
def get_peer_group(
    group_name: str
):
    conn = get_connection()
    query = """

SELECT

pg.company_id,

REPLACE(c.company_name,char(10),' ') AS company_name,

pg.is_benchmark

FROM peer_groups pg

JOIN companies c

ON pg.company_id=c.id

WHERE

pg.peer_group_name=?

ORDER BY

pg.is_benchmark DESC,

company_name

"""
    peer_df = pd.read_sql(

    query,

    conn,

    params=[group_name]

)
    if peer_df.empty:

        conn.close()

        raise HTTPException(

        status_code=404,

        detail="Peer group not found"

    )
    percentiles = pd.read_sql(
    """

SELECT *

FROM peer_percentiles

WHERE

peer_group_name=?

AND

year=(

SELECT MAX(year)

FROM peer_percentiles p2

WHERE

p2.company_id=peer_percentiles.company_id

)

""",

    conn,

    params=[group_name]

)
    conn.close()
    pivot = percentiles.pivot_table(

    index="company_id",

    columns="metric",

    values="percentile_rank"

).reset_index()
    peer_df = peer_df.merge(

    pivot,

    on="company_id",

    how="left"

)
    return peer_df.to_dict(
    orient="records"
)