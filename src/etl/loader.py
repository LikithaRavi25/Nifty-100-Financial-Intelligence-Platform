# src/etl/loader.py

import time
import pandas as pd

from pathlib import Path

from src.etl.config import (
    CORE_FILES,
    ALL_FILES
)

from src.etl.normalizer import (
    clean_column_name,
    normalize_dataframe
)

from src.etl.audit import (
    add_audit_entry
)


def validate_files_exist():

    root = Path("data/raw")

    missing = []

    for file in ALL_FILES:

        if not (root / file).exists():
            missing.append(file)

    return missing


def load_excel(file_path):

    filename = file_path.name.lower()

    if filename in CORE_FILES:
        header_row = 1
    else:
        header_row = 0

    start = time.time()

    df = pd.read_excel(
        file_path,
        header=header_row,
        engine="openpyxl"
    )

    df.columns = [
        clean_column_name(c)
        for c in df.columns
    ]

    df = normalize_dataframe(df)

    runtime = time.time() - start

    add_audit_entry(
        table_name=file_path.stem,
        rows_in=len(df),
        rows_out=len(df),
        runtime_s=runtime
    )

    return df


def load_all_files():

    root = Path("data/raw")

    dataframes = {}

    for file in root.glob("*.xlsx"):

        print(f"Loading {file.name}")

        df = load_excel(file)

        dataframes[file.stem] = df

    return dataframes