import sqlite3
import pandas as pd
from pathlib import Path
from tearsheet import generate_tearsheet

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "nifty100.db"
OUTPUT_DIR = BASE_DIR / "output"

conn = sqlite3.connect(DB_PATH)

companies = pd.read_sql("""
SELECT id, company_name
FROM companies
ORDER BY id
""", conn)

print(companies.head())
print("Total Companies:", len(companies))

success = 0
failed = []

for company in companies["id"]:

    try:
        skipped = []
        query = f"""
        SELECT COUNT(DISTINCT year) AS total_years
        FROM financial_ratios
        WHERE company_id='{company}'
        """

        years = pd.read_sql(query, conn).iloc[0]["total_years"]

        if years < 3:
            skipped.append((company, years))
            continue

        print("Generating", company)

        generate_tearsheet(company)

        success += 1

    except Exception as e:

        failed.append((company, str(e)))

skipped_df = pd.DataFrame(
    skipped,
    columns=[
        "company_id",
        "years_available"
    ]
)

skipped_df.to_csv(
    OUTPUT_DIR / "skipped_tearsheets.csv",
    index=False
)

print("✅ skipped_tearsheets.csv saved")
print()

print("="*50)

print("Batch Generation Complete")

print("="*50)

print("Generated :", success)

print("Failed :", len(failed))

for f in failed:

    print(f)

import pandas as pd

errors = pd.DataFrame(
    failed,
    columns=[
        "company_id",
        "error"
    ]
)

errors.to_csv(
    OUTPUT_DIR /
    "report_generation_errors.csv",
    index=False
)

print(
    "report_generation_errors.csv saved"
)
        

