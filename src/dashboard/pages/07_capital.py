import streamlit as st
import pandas as pd
import plotly.express as px

from utils.db import get_capital_allocation_data



st.title("💰 Capital Allocation Map")

st.markdown(
    """
    Visualize companies based on inferred capital allocation strategies.
    """
)

st.divider()

df = get_capital_allocation_data()


def assign_capital_pattern(row):

    # Quality Compounder
    if (
        row["return_on_equity_pct"] >= 20
        and row["free_cash_flow_cr"] > 0
        and row["debt_to_equity"] <= 0.5
    ):
        return "Quality Compounder"

    # Growth Investment
    elif (
        row["revenue_cagr_5yr"] >= 15
        and row["pat_cagr_5yr"] >= 15
    ):
        return "Growth Investment"

    # Dividend Focus
    elif row["dividend_payout"] >= 30:
        return "Dividend Focus"

    # Expansion
    elif row["capex_cr"] > 1000:
        return "Expansion"

    # Debt Reduction
    elif row["debt_to_equity"] > 1:
        return "Debt Reduction"

    # Cash Rich
    elif row["free_cash_flow_cr"] > 5000:
        return "Cash Rich"

    # Stable Business
    elif (
        row["return_on_equity_pct"] >= 10
        and row["revenue_cagr_5yr"] >= 5
    ):
        return "Stable Business"

    # Default
    else:
        return "Balanced Allocation"
    
df["capital_pattern"] = df.apply(
    assign_capital_pattern,
    axis=1
)

st.subheader("📊 Capital Allocation Summary")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Companies",
    len(df)
)

col2.metric(
    "Allocation Patterns",
    df["capital_pattern"].nunique()
)

col3.metric(
    "Largest Pattern",
    df["capital_pattern"].value_counts().idxmax()
)

selected_pattern = st.selectbox(
    "Filter by Capital Allocation Pattern",
    ["All"] + sorted(df["capital_pattern"].unique())
)

if selected_pattern != "All":
    display_df = df[
        df["capital_pattern"] == selected_pattern
    ]
else:
    display_df = df
    
fig = px.treemap(
    display_df,
    path=[
        "capital_pattern",
        "company_name"
    ],
    values="market_cap_crore",
    color="capital_pattern",
    hover_data=[
        "return_on_equity_pct",
        "debt_to_equity",
        "revenue_cagr_5yr",
        "free_cash_flow_cr"
    ],
    title="Capital Allocation Strategy Map"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("🏢 Companies")

st.dataframe(

    display_df[
        [
            "company_name",
            "capital_pattern",
            "market_cap_crore",
            "return_on_equity_pct",
            "debt_to_equity",
            "free_cash_flow_cr"
        ]
    ],

    use_container_width=True,
    hide_index=True
)