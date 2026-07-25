import streamlit as st
import pandas as pd
import plotly.graph_objects as go


from utils.db import (
    get_company_master,
    get_company_details,
    get_company_peer_group,
    get_latest_ratios,
    get_company_profit_history,
    get_company_ratio_history
)

def generate_pros_cons(data):

    pros = []
    cons = []

    # ROE
    if data["return_on_equity_pct"] >= 15:
        pros.append("High ROE (>15%)")
    else:
        cons.append("Low ROE")

    # Debt
    if data["debt_to_equity"] <= 1:
        pros.append("Low Debt")
    else:
        cons.append("High Debt")

    # Revenue CAGR
    if data["revenue_cagr_5yr"] >= 10:
        pros.append("Strong Revenue Growth")
    else:
        cons.append("Weak Revenue Growth")

    # Free Cash Flow
    if data["free_cash_flow_cr"] > 0:
        pros.append("Positive Free Cash Flow")
    else:
        cons.append("Negative Free Cash Flow")

    # Interest Coverage
    if data["interest_coverage"] >= 3:
        pros.append("Healthy Interest Coverage")
    else:
        cons.append("Weak Interest Coverage")

    # Net Profit Margin
    if data["net_profit_margin_pct"] >= 10:
        pros.append("Good Profit Margin")
    else:
        cons.append("Low Profit Margin")

    return pros, cons

st.title("🏢 Company Profile")

companies = get_company_master()

company_list = (
    companies["company_name"]
    + " ("
    + companies["id"]
    + ")"
)

selected = st.selectbox(
    "Search Company",
    company_list
)

ticker = selected.split("(")[-1].replace(")", "")


company = get_company_details(ticker)

peer = get_company_peer_group(ticker)

if company.empty:

    st.error("Company not found.")

    st.stop()

company = company.iloc[0]

peer_group = (
    peer.iloc[0]["peer_group_name"]
    if not peer.empty
    else "Not Assigned"
)

latest = get_latest_ratios(ticker)

if latest.empty:

    st.warning("No financial ratios available.")

    st.stop()

latest = latest.iloc[0]
pros, cons = generate_pros_cons(latest)
history = get_company_profit_history(ticker)
ratio_history = get_company_ratio_history(ticker)

left, right = st.columns([1,3])

with left:

    logo = company["company_logo"]

    if (
    pd.notna(logo)
    and str(logo).startswith("http")
):
        st.image(
        logo,
        width=140
    )
    else:
        st.info("🏢 Logo unavailable")

with right:

    st.title(company["company_name"])

    st.caption(f"NSE : {company['id']}")

    st.markdown(
    f"**🏭 Peer Group:** {peer_group}"
)

    st.markdown(
    f"**🌐 Website:** {company['website']}"
)

    st.divider()

    st.subheader("📊 Latest Financial KPIs")

    row1 = st.columns(3)

    with row1[0]:
        st.metric(
        "ROE",
        f"{latest['return_on_equity_pct']:.2f}%"
    )

    with row1[1]:
        st.metric(
        "ROCE",
        f"{latest['return_on_capital_employed_pct']:.2f}%"
    )

    with row1[2]:
        st.metric(
        "Net Profit Margin",
        f"{latest['net_profit_margin_pct']:.2f}%"
    )
        
    row2 = st.columns(3)

    with row2[0]:
        st.metric(
        "Debt / Equity",
        round(latest["debt_to_equity"], 2)
    )

    with row2[1]:
        st.metric(
        "Revenue CAGR (5Y)",
        f"{latest['revenue_cagr_5yr']:.2f}%"
    )

    with row2[2]:
        st.metric(
        "Free Cash Flow",
        f"₹ {latest['free_cash_flow_cr']:.0f} Cr"
    )

    st.markdown("---")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
        "Book Value",
        company["book_value"]
    )

    with c2:
        st.metric(
        "ROE",
        f"{company['roe_percentage']}%"
    )

    with c3:
        st.metric(
        "ROCE",
        f"{company['roce_percentage']}%"
    )
        
    st.divider()

    st.subheader("📊 Revenue & Net Profit (10 Years)")
    fig = go.Figure()

    fig.add_trace(
    go.Bar(
        x=history["year"],
        y=history["sales"],
        name="Revenue"
    )
)

    fig.add_trace(
    go.Bar(
        x=history["year"],
        y=history["net_profit"],
        name="Net Profit"
    )
)

    fig.update_layout(

    barmode="group",

    height=500,

    xaxis_title="Financial Year",

    yaxis_title="₹ Crore",

    legend_title="Metric"
)

    st.plotly_chart(
    fig,
    use_container_width=True
)
    
    st.divider()
    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()

    st.subheader("📈 ROE & ROCE Trend (10 Years)")
    fig = go.Figure()

    fig.add_trace(
    go.Scatter(
        x=ratio_history["year"],
        y=ratio_history["return_on_equity_pct"],
        mode="lines+markers",
        name="ROE",
        yaxis="y1"
    )
)

    fig.add_trace(
    go.Scatter(
        x=ratio_history["year"],
        y=ratio_history["return_on_capital_employed_pct"],
        mode="lines+markers",
        name="ROCE",
        yaxis="y2"
    )
)

    fig.update_layout(

    height=500,

    xaxis=dict(
        title="Financial Year"
    ),

    yaxis=dict(
        title="ROE (%)"
    ),

    yaxis2=dict(
        title="ROCE (%)",
        overlaying="y",
        side="right"
    ),

    legend=dict(
        orientation="h"
    )
)

    st.plotly_chart(
    fig,
    use_container_width=True
)
    st.divider()

    st.subheader("👍 Strengths & ⚠️ Weaknesses")
    left, right = st.columns(2)
    with left:

        st.success("Strengths")

        if pros:
            for item in pros:
                st.markdown(f"✅ {item}")
        else:
            st.write("No major strengths identified.")

    with right:

        st.error("Weaknesses")

        if cons:
            for item in cons:
                st.markdown(f"❌ {item}")
        else:
            st.write("No major weaknesses identified.")