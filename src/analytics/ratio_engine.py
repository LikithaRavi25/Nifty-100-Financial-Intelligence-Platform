import sqlite3
import pandas as pd

from ratios import *
from cagr import *
from cashflow_kpis import *
from composite_score import composite_quality_score


from edge_logger import (
    reset_log,
    log_case
)

def load_tables():

    conn = sqlite3.connect("nifty100.db")

    profit = pd.read_sql(
        "SELECT * FROM profitandloss",
        conn
    )

    balance = pd.read_sql(
        "SELECT * FROM balancesheet",
        conn
    )

    cashflow = pd.read_sql(
        "SELECT * FROM cashflow",
        conn
    )

    companies = pd.read_sql(
        "SELECT * FROM companies",
        conn
    )

    conn.close()

    return (
        profit,
        balance,
        cashflow,
        companies
    )

    
if __name__ == "__main__":
    reset_log()
    (
        profit,
        balance,
        cashflow,
        companies
    ) = load_tables()

    print("\n==============================")
    print("DUPLICATE CHECK")
    print("==============================")

    print(
    "Profit duplicates :",
    profit.duplicated(
        subset=["company_id", "year"]
    ).sum()
)

    print(
    "Balance duplicates:",
    balance.duplicated(
        subset=["company_id", "year"]
    ).sum()
)

    print(
    "Cashflow duplicates:",
    cashflow.duplicated(
        subset=["company_id", "year"]
    ).sum()
)

    print("\nChecking duplicates...\n")

    print(
    "Profit:",
    profit.duplicated(
        ["company_id","year"]
    ).sum()
)

    print(
    "Balance:",
    balance.duplicated(
        ["company_id","year"]
    ).sum()
)

    print(
    "Cashflow:",
    cashflow.duplicated(
        ["company_id","year"]
    ).sum()
)
    print("\nMerging Profit & Loss with Balance Sheet...")

    master = profit.merge(
    balance,
    on=["company_id", "year"],
    how="inner",
    suffixes=("_pl", "_bs")
)

    print(master.shape)

    print("\nMerging Cash Flow...")

    master = master.merge(
    cashflow,
    on=["company_id", "year"],
    how="inner"
)

    print(master.shape)

    print("\nMerging Companies...")

    master = master.merge(
    companies,
    left_on="company_id",
    right_on="id",
    how="left"
)

    print(master.shape)
    print("\nMASTER DATASET\n")
    print(master.head())
    print()
    print(master.columns.tolist())
    print("\nSorting Master Dataset...\n")

    master = master.sort_values(
    ["company_id", "year"]
).reset_index(drop=True)

    print("\nTABLES LOADED\n")

    print(
        f"Profit & Loss : {profit.shape}"
    )

    print(
        f"Balance Sheet : {balance.shape}"
    )

    print(
        f"Cash Flow     : {cashflow.shape}"
    )

    print(
        f"Companies     : {companies.shape}"
    )


    print("\nCalculating Net Profit Margin...")

    master["net_profit_margin_pct"] = master.apply(
    lambda row: net_profit_margin(
        row["net_profit"],
        row["sales"]
    ),
    axis=1
)
    
    print(
    master[
        [
            "company_id",
            "year",
            "operating_profit",
            "sales",
            "opm_percentage"
        ]
    ].loc[master["opm_percentage"] > 100].head(20)
)
    
    print("Calculating Operating Profit Margin...")

    master["operating_profit_margin_pct"] = master.apply(
    lambda row: operating_profit_margin(
        row["operating_profit"],
        row["sales"],
        row["opm_percentage"]
    ),
    axis=1
)

    print("Calculating ROE...")

    master["return_on_equity_pct"] = master.apply(
    lambda row: return_on_equity(
        row["net_profit"],
        row["equity_capital"],
        row["reserves"]
    ),
    axis=1
)
    print(
    master[
        [
            "company_id",
            "year",
            "return_on_equity_pct",
            "roe_percentage"
        ]
    ].head()
)
    
    print("Calculating Debt to Equity...")

    master["debt_to_equity"] = master.apply(
    lambda row: debt_to_equity(
        row["borrowings"],
        row["equity_capital"],
        row["reserves"]
    ),
    axis=1
)

    print("Generating High Leverage Flag...")

    master["high_leverage_warning"] = master.apply(
    lambda row: high_leverage_flag(
        row["debt_to_equity"],
        row["company_id"]
    ),
    axis=1
)
    print("\nHigh Leverage Warning Sample\n")

    print(
    master[
        [
            "company_id",
            "debt_to_equity",
            "high_leverage_warning"
        ]
    ].head(20)
)
    print("Calculating Interest Coverage...")



    master["interest_coverage"] = master.apply(
    lambda row: interest_coverage_ratio(
        row["operating_profit"],
        row["other_income"],
        row["interest"]
    ),
    axis=1
)
    print("Calculating Asset Turnover...")

    master["asset_turnover"] = master.apply(
    lambda row: asset_turnover(
        row["sales"],
        row["total_assets"]
    ),
    axis=1
)
    print("Calculating Free Cash Flow...")

    master["free_cash_flow_cr"] = master.apply(
    lambda row: free_cash_flow(
        row["operating_activity"],
        row["investing_activity"]
    ),
    axis=1
)
    print("Calculating CapEx Intensity...")

    master["capex_cr"] = master.apply(
    lambda row: capex_intensity(
        row["investing_activity"],
        row["sales"]
    ),
    axis=1
)
    print("Calculating CFO Quality Score...")

    master["cfo_quality_score"] = master.apply(
    lambda row: cfo_quality_score(
        row["operating_activity"],
        row["net_profit"]
    ),
    axis=1
)
    print("Calculating FCF Conversion...")

    master["fcf_conversion_rate"] = master.apply(
    lambda row: fcf_conversion_rate(
        row["free_cash_flow_cr"],
        row["operating_profit"]
    ),
    axis=1
)
    
    print("Calculating ROCE...")

    master["return_on_capital_employed_pct"] = master.apply(
    lambda row: return_on_capital_employed(
        row["operating_profit"] + row["other_income"],
        row["equity_capital"],
        row["reserves"],
        row["borrowings"]
    ),
    axis=1
)
    print(
    master[
        [
            "company_id",
            "year",
            "return_on_capital_employed_pct",
            "roce_percentage"
        ]
    ].head()
)
    print("Calculating ROA...")

    master["return_on_assets_pct"] = master.apply(
    lambda row: return_on_assets(
        row["net_profit"],
        row["total_assets"]
    ),
    axis=1
)

    print("Calculating Net Debt...")

    master["total_debt_cr"] = master.apply(
    lambda row: net_debt(
        row["borrowings"],
        row["investments"]
    ),
    axis=1
)
    
    print("Calculating 5-Year CAGR Metrics...")

    master["revenue_cagr_5yr"] = None
    master["pat_cagr_5yr"] = None
    master["eps_cagr_5yr"] = None

    companies = master["company_id"].unique()

    for company in companies:

        company_data = master[
        master["company_id"] == company
    ].sort_values("year")

        indices = company_data.index.tolist()

        for i in range(5, len(indices)):
 
            current = indices[i]
            previous = indices[i - 5]

            rev, _ = revenue_cagr(
            master.loc[previous, "sales"],
            master.loc[current, "sales"],
            5
        )

            pat, _ = pat_cagr(
            master.loc[previous, "net_profit"],
            master.loc[current, "net_profit"],
            5
        )

            eps, _ = eps_cagr(
            master.loc[previous, "eps"],
            master.loc[current, "eps"],
            5
        )

            master.loc[current, "revenue_cagr_5yr"] = rev
            master.loc[current, "pat_cagr_5yr"] = pat
            master.loc[current, "eps_cagr_5yr"] = eps

    print("5-Year CAGR calculation completed.")

    print("\n5-Year CAGR Sample\n")

    print(
    master[
        [
            "company_id",
            "year",
            "revenue_cagr_5yr",
            "pat_cagr_5yr",
            "eps_cagr_5yr"
        ]
    ].tail(20)
)



    
    print("\nChecking ROCE Edge Cases...")

    for _, row in master.iterrows():

       calculated = row["return_on_capital_employed_pct"]
       source = row["roce_percentage"]

       if pd.notna(calculated) and pd.notna(source):

           difference = abs(calculated - source)

           if difference > 5:

             log_case(
                company=row["company_id"],
                year=row["year"],
                ratio="ROCE",
                calculated=calculated,
                source=source,
                category="Formula Difference"
            )

    print("ROCE validation completed.")

    print("\nChecking ROE Edge Cases...")

    for _, row in master.iterrows():

        calculated = row["return_on_equity_pct"]
        source = row["roe_percentage"]

        if pd.notna(calculated) and pd.notna(source):

           difference = abs(calculated - source)

           if difference > 5:

                if source < 1:
                    category = "Source Data Issue"

                elif difference > 20:
                    category = "Version Difference"

                else:
                    category = "Formula Discrepancy"

                log_case(
                company=row["company_id"],
                year=row["year"],
                ratio="ROE",
                calculated=calculated,
                source=source,
                category=category
            )

    print("ROE validation completed.")   

    print("Calculating Composite Quality Score...")

    master["composite_quality_score"] = composite_quality_score(master)  

    print("\nComputed KPI Columns:\n")

    print(
    master[
        [
            "company_id",
            "year",
            "net_profit_margin_pct",
            "return_on_equity_pct",
            "debt_to_equity",
            "interest_coverage",
            "asset_turnover",
            "free_cash_flow_cr",
            "composite_quality_score"
        ]
    ].head()
)
    
    print("\nSaving financial ratios to SQLite...")

    conn = sqlite3.connect("nifty100.db")

    columns = [
    "company_id",
    "year",

    # Profitability
    "net_profit_margin_pct",
    "operating_profit_margin_pct",
    "return_on_equity_pct",
    "return_on_capital_employed_pct",
    "return_on_assets_pct",

    # Leverage
    "debt_to_equity",
    "interest_coverage",
    "total_debt_cr",
    "high_leverage_warning",

    # Efficiency
    "asset_turnover",

    # Cash Flow
    "free_cash_flow_cr",
    "capex_cr",
    "cfo_quality_score",
    "fcf_conversion_rate",
    "revenue_cagr_5yr",
"pat_cagr_5yr",
"eps_cagr_5yr",

    "sales",
    "eps",
    "book_value",
    "dividend_payout",
    "composite_quality_score"
]

    master[columns].to_sql(
    "financial_ratios",
    conn,
    if_exists="replace",
    index=False
)

    conn.close()

    print("financial_ratios table populated successfully.")

    print("\n======================================")
    print("DAY 12 COMPLETED SUCCESSFULLY")
    print("======================================")
    print(f"Financial Ratios Generated : {len(master)}")
    print("SQLite table updated.")
    print("Ready for Day 13.")

    

    