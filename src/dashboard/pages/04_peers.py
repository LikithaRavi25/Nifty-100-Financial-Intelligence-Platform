import streamlit as st
import plotly.graph_objects as go
from utils.db import (
    get_peer_groups,
    get_peer_companies,
    get_peer_metrics,
    get_peer_kpi_table
)

st.title("👥 Peer Comparison")

st.markdown(
    "Compare a company against its peer group using financial metrics."
)

st.divider()

st.subheader("📂 Select Peer Group")

groups = get_peer_groups()

peer_group = st.selectbox(
    "Peer Group",
    groups["peer_group_name"]
)

companies = get_peer_companies(peer_group)

company = st.selectbox(
    "Company",
    companies["company_name"]
)
peer_df = get_peer_metrics(peer_group)
company_row = peer_df[
    peer_df["company_name"] == company
].iloc[0]

metrics = [

    "return_on_equity_pct",

    "return_on_capital_employed_pct",

    "net_profit_margin_pct",

    "operating_profit_margin_pct",

    "asset_turnover",

    "interest_coverage",

    "free_cash_flow_cr",

    "debt_to_equity"

]

peer_avg = peer_df[
    metrics
].mean()

fig = go.Figure()

fig.add_trace(

    go.Scatterpolar(

        r=[
            company_row[m]
            for m in metrics
        ],

        theta=[
            "ROE",
            "ROCE",
            "NPM",
            "OPM",
            "Asset Turnover",
            "Interest Coverage",
            "Free Cash Flow",
            "Debt/Equity"
        ],

        fill="toself",

        name=company

    )

)

fig.add_trace(

    go.Scatterpolar(

        r=[
            peer_avg[m]
            for m in metrics
        ],

        theta=[
            "ROE",
            "ROCE",
            "NPM",
            "OPM",
            "Asset Turnover",
            "Interest Coverage",
            "Free Cash Flow",
            "Debt/Equity"
        ],

        fill="toself",

        name="Peer Average"

    )

)

fig.update_layout(

    polar=dict(

        radialaxis=dict(

            visible=True

        )

    ),

    showlegend=True,

    height=650
)

st.subheader("📊 Company vs Peer Group")

st.plotly_chart(
    fig,
    use_container_width=True
)

peer_table = get_peer_kpi_table(peer_group)
st.subheader("📋 Peer Comparison Table")

def highlight_benchmark(row):

    if row["is_benchmark"] == 1:
        return [
            "background-color:#FFD966"
        ] * len(row)

    return [""] * len(row)

st.dataframe(
    peer_table.style.apply(
        highlight_benchmark,
        axis=1
    ),
    use_container_width=True
)

csv = peer_table.drop(
    columns=["is_benchmark"]
).to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇ Download Peer Comparison CSV",
    data=csv,
    file_name=f"{peer_group}_peer_comparison.csv",
    mime="text/csv"
)

download_df = peer_table.drop(
    columns=["is_benchmark"]
)

csv = download_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    "⬇ Download CSV",
    csv,
    file_name=f"{peer_group}_comparison.csv",
    mime="text/csv"
)