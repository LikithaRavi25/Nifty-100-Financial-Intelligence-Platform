# src/validators/validator.py

import pandas as pd

from etl.rules import (
    check_company_id_not_null,
    check_duplicate_company_year,
    check_sales_positive,
    check_balance_sheet,
    check_cashflow_totals,
    check_opm,
    check_year_format,
    check_url_columns
)

all_failures = []


def validate_table(
    df,
    table_name
):

    global all_failures

    checks = [

        check_company_id_not_null,
        check_duplicate_company_year,
        check_sales_positive,
        check_balance_sheet,
        check_cashflow_totals,
        check_opm,
        check_year_format,
        check_url_columns

    ]

    for check in checks:

        try:

            failures = check(
                df,
                table_name
            )

            all_failures.extend(
                failures
            )

        except Exception as e:

            print(
                f"Validation Error ({table_name}) : {e}"
            )


def save_validation_report():

    df = pd.DataFrame(
        all_failures
    )

    df.to_csv(
        "validation_failures.csv",
        index=False
    )

    print(
        f"Validation report generated: {len(df)} issues"
    )