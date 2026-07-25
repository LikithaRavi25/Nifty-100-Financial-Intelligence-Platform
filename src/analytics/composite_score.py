import pandas as pd
import numpy as np

def normalize_score(series):
    """
    Normalize a pandas Series to a 0–100 score
    using 10th/90th percentile winsorization.
    """

    series = series.copy()

    # Ignore missing values
    valid = series.dropna()

    if len(valid) == 0:
        return series

    # Calculate 10th and 90th percentiles
    p10 = valid.quantile(0.10)
    p90 = valid.quantile(0.90)

    # Winsorize (clip extreme values)
    series = series.clip(lower=p10, upper=p90)

    # Avoid division by zero
    if p90 == p10:
        return pd.Series(
            100,
            index=series.index
        )

    # Scale to 0–100
    score = (
        (series - p10)
        /
        (p90 - p10)
    ) * 100

    return score.round(2)

def profitability_score(df):
    """
    Calculate Profitability Score (35%)
    """

    roe = normalize_score(
    df["return_on_equity_pct"]
)

    roce = normalize_score(
    df["return_on_capital_employed_pct"]
)

    npm = normalize_score(
    df["net_profit_margin_pct"]
)
    
    score = (

    roe * 0.15 +

    roce * 0.10 +

    npm * 0.10

)
    
    return score.round(2)

def cash_quality_score(df):
    """
    Calculate Cash Quality Score (30%)
    """
    fcf = normalize_score(
    df["free_cash_flow_cr"]
)
    cfo = normalize_score(
    df["cfo_quality_score"]
)
    fcf_positive = (
    df["free_cash_flow_cr"] > 0
).astype(int) * 100
    
    score = (

    fcf * 0.15 +

    cfo * 0.10 +

    fcf_positive * 0.05

)
    return score.round(2)

def growth_score(df):
    """
    Calculate Growth Score (20%)
    """

    if (
        "revenue_cagr_5yr" not in df.columns or
        "pat_cagr_5yr" not in df.columns
    ):
        return pd.Series(
            0,
            index=df.index
        )

    revenue = normalize_score(
        df["revenue_cagr_5yr"]
    )

    pat = normalize_score(
        df["pat_cagr_5yr"]
    )

    score = (

        revenue * 0.10 +

        pat * 0.10

    )

    return score.round(2)

def leverage_score(df):
    """
    Calculate Leverage Score (15%)
    """

    de = normalize_score(
        df["debt_to_equity"]
    )

    de = 100 - de

    icr = normalize_score(
        df["interest_coverage"].fillna(
            df["interest_coverage"].max()
        )
    )

    score = (

        de * 0.10 +

        icr * 0.05

    )

    return score.round(2)

def composite_quality_score(df):

    profit = profitability_score(df)

    cash = cash_quality_score(df)

    growth = growth_score(df)

    leverage = leverage_score(df)

    score = (

        profit +

        cash +

        growth +

        leverage

    )

    return score.round(2)

if __name__ == "__main__":

    import sqlite3

    conn = sqlite3.connect("nifty100.db")

    df = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn
    )

    conn.close()

    df["leverage_score"] = leverage_score(df)

    print(
    df[
        [
            "company_id",
            "year",
            "leverage_score"
        ]
    ].head()
)