# src/database/loader.py

from src.database.db import get_connection


def load_dataframe(df, table_name):

    conn = get_connection()

    df.to_sql(
        table_name,
        conn,
        if_exists="replace",
        index=False
    )

    conn.commit()
    conn.close()

    print(f"Loaded {table_name}")