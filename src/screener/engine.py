

import sys
import os

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.append(BASE_DIR)
sys.path.append(os.path.dirname(__file__))

import sqlite3
import pandas as pd

from analytics.composite_score import composite_quality_score
from presets import PRESETS
from config_loader import load_config




def load_financial_ratios():

    conn = sqlite3.connect("nifty100.db")

    df = pd.read_sql(
    """
    SELECT *
    FROM financial_ratios
    """,
    conn
)
    print(df.columns.tolist())

    conn.close()

    return df


def apply_filters(df, config):
    filters = config


    # ROE
    if filters["roe_min"] is not None:
        df = df[
            df["return_on_equity_pct"] >= filters["roe_min"]
        ]

    # Debt to Equity
    if filters["debt_to_equity_max"] is not None:
        df = df[
        df["debt_to_equity"] <= filters["debt_to_equity_max"]
    ]

    # Interest Coverage
    if filters["interest_coverage_min"] is not None:

        df = df[
        (
            df["interest_coverage"] >= filters["interest_coverage_min"]
        )
        |
        (
            df["interest_coverage"].isna()
        )
    ]

    # Asset Turnover
    if filters["asset_turnover_min"] is not None:
        df = df[
            df["asset_turnover"] >= filters["asset_turnover_min"]
        ]

    # Free Cash Flow
    if filters["free_cash_flow_min"] is not None:
        df = df[
            df["free_cash_flow_cr"] >= filters["free_cash_flow_min"]
        ]


        # Revenue CAGR
    if filters["revenue_cagr_min"] is not None:
        df = df[
            df["revenue_cagr_5yr"] >= filters["revenue_cagr_min"]
        ]

    # PAT CAGR
    if filters["pat_cagr_min"] is not None:
        df = df[
            df["pat_cagr_5yr"] >= filters["pat_cagr_min"]
        ]

    # EPS CAGR
    if filters["eps_cagr_min"] is not None:
        df = df[
            df["eps_cagr_5yr"] >= filters["eps_cagr_min"]
        ]

    # Operating Profit Margin
    if filters["operating_profit_margin_min"] is not None:
        df = df[
            df["operating_profit_margin_pct"] >= filters["operating_profit_margin_min"]
        ]

    # Dividend Payout
    if filters["dividend_payout_max"] is not None:
        df = df[
            df["dividend_payout"] <= filters["dividend_payout_max"]
        ]

    # Book Value
    if filters["book_value_min"] is not None:
        df = df[
            df["book_value"] >= filters["book_value_min"]
        ]

    # Earnings Per Share
    if filters["earnings_per_share_min"] is not None:
        df = df[
            df["earnings_per_share"] >= filters["earnings_per_share_min"]
        ]

    # CapEx
    if filters["capex_max"] is not None:
        df = df[
            df["capex_cr"] <= filters["capex_max"]
        ]

    # Total Debt
    if filters["total_debt_max"] is not None:
        df = df[
            df["total_debt_cr"] <= filters["total_debt_max"]
        ]

    # Sales
    if filters["sales_min"] is not None:
        df = df[
            df["sales"] >= filters["sales_min"]
        ]
        

    df["composite_quality_score"] = (
    df["return_on_equity_pct"].fillna(0)
    + df["operating_profit_margin_pct"].fillna(0)
    + df["asset_turnover"].fillna(0) * 10
    + df["interest_coverage"].fillna(0)
)   
    
    df = df.sort_values(
    by="composite_quality_score",
    ascending=False
)
    return df


def load_preset(name):

    if name not in PRESETS:
        raise ValueError(
            f"Unknown preset: {name}"
        )

    return PRESETS[name]

def run_screener():

    config = load_config()

    PRESET_NAME = "turnaround_watch"  # Change this to the desired preset name

    preset = load_preset(PRESET_NAME)

    print("\nActive Preset")
    print("=================")
    print(PRESET_NAME.replace("_", " ").title())
    print("\nActive Preset")
    print("=================")
    print("Turnaround Watch\n")

    config["filters"].update(
        preset
    )

    df = load_financial_ratios()

    df = apply_filters(
        df,
        config["filters"]
    )
    df["composite_quality_score"] = composite_quality_score(df)


    df = df.sort_values(
    by="composite_quality_score",
    ascending=False
)

    return df


if __name__ == "__main__":

    result = run_screener()

    print("\nResult Preview")

    print(result[
    [
        "company_id",
        "year",
        "return_on_equity_pct",
        "debt_to_equity",
            "interest_coverage",
            "composite_quality_score"

    ]
].head(20))

    print("\nRows Returned:", len(result))


    import os
    import pandas as pd

    os.makedirs("output", exist_ok=True)

    writer = pd.ExcelWriter(
    "output/screener_output.xlsx",
    engine="openpyxl"
)

    for preset in PRESETS.keys():

        print(f"\nRunning {preset}...")

        config = load_config()

        config["preset"] = preset

        config["filters"] = PRESETS[preset]

        result = run_screener()

        result.to_excel(
        writer,
        sheet_name=preset,
        index=False
    )

        print(
        f"{preset}: {len(result)} companies"
    )

    writer.close()

    print("\nAll preset screeners exported successfully.")
    print(pd.read_sql(
    "SELECT * FROM financial_ratios LIMIT 1",
    sqlite3.connect("nifty100.db")
).columns.tolist())