# src/etl/audit.py

import pandas as pd
from datetime import datetime


audit_rows = []


def add_audit_entry(
    table_name,
    rows_in,
    rows_out,
    runtime_s
):

    audit_rows.append({
        "table": table_name,
        "rows_in": rows_in,
        "rows_out": rows_out,
        "runtime_s": round(runtime_s, 2),
        "timestamp": datetime.now()
    })


def save_audit():

    df = pd.DataFrame(audit_rows)

    df.to_csv(
        "load_audit.csv",
        index=False
    )