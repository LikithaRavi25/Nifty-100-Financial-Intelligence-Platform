import streamlit as st
from utils.db import get_screener_data

st.title("🔍 Stock Screener")

st.markdown(
"""
Filter companies using financial metrics
and predefined investment presets.
"""
)

st.divider()



df = get_screener_data()

st.sidebar.header("📊 Filter Stocks")
roe = st.sidebar.slider(
    "Minimum ROE (%)",
    min_value=0.0,
    max_value=50.0,
    value=15.0,
    step=1.0
)
de = st.sidebar.slider(
    "Maximum Debt/Equity",
    min_value=0.0,
    max_value=5.0,
    value=1.0,
    step=0.1
)
fcf = st.sidebar.slider(
    "Minimum Free Cash Flow (₹ Cr)",
    min_value=float(df["free_cash_flow_cr"].min()),
    max_value=float(df["free_cash_flow_cr"].max()),
    value=0.0
)
revenue = st.sidebar.slider(
    "Minimum Revenue CAGR (5Y)",
    min_value=-50.0,
    max_value=50.0,
    value=10.0
)
pat = st.sidebar.slider(
    "Minimum PAT CAGR (5Y)",
    min_value=-50.0,
    max_value=50.0,
    value=10.0
)
opm = st.sidebar.slider(
    "Minimum OPM (%)",
    min_value=0.0,
    max_value=70.0,
    value=15.0
)
dividend = st.sidebar.slider(
    "Minimum Dividend Payout",
    min_value=0.0,
    max_value=100.0,
    value=0.0
)
icr = st.sidebar.slider(
    "Minimum Interest Coverage",
    min_value=0.0,
    max_value=100.0,
    value=3.0
)

book = st.sidebar.slider(
    "Minimum Book Value",
    min_value=float(df["book_value"].min()),
    max_value=float(df["book_value"].max()),
    value=float(df["book_value"].min())
)

st.subheader("📌 Quick Presets")

col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

quality = col1.button("⭐ Quality")
value = col2.button("💰 Value")
growth = col3.button("📈 Growth")

dividend_btn = col4.button("💵 Dividend")
debtfree = col5.button("🛡️ Debt Free")
turnaround = col6.button("🔄 Turnaround")

if quality:
    roe = 20.0
    de = 1.0
    revenue = 10.0
    pat = 10.0
    opm = 15.0

if value:
    roe = 15.0
    de = 2.0
    revenue = 5.0
    pat = 5.0
    opm = 10.0

if growth:
    roe = 15.0
    revenue = 20.0
    pat = 20.0

if dividend_btn:
    dividend = 30.0

if debtfree:
    de = 0.5

if turnaround:
    roe = 5.0
    de = 3.0
    revenue = 5.0

filtered = df.copy()
st.write("Initial:", len(filtered))

filtered = filtered[
    filtered["return_on_equity_pct"] >= roe
]
st.write("After ROE:", len(filtered))

filtered = filtered[
    filtered["debt_to_equity"] <= de
]
st.write("After Debt:", len(filtered))

filtered = filtered[
    filtered["free_cash_flow_cr"] >= fcf
]
st.write("After FCF:", len(filtered))

filtered = filtered[
    filtered["revenue_cagr_5yr"] >= revenue
]
st.write("After revenue CAGR:", len(filtered))

filtered = filtered[
    filtered["pat_cagr_5yr"] >= pat
]
st.write("After PAT CAGR:", len(filtered))
filtered = filtered[
    filtered["operating_profit_margin_pct"] >= opm
]
st.write("After OPM:", len(filtered))
filtered = filtered[
    filtered["dividend_payout"] >= dividend
]
st.write("After Dividend:", len(filtered))

filtered = filtered[
    filtered["interest_coverage"] >= icr
]
st.write("After ICR:", len(filtered))

filtered = filtered[
    filtered["book_value"] >= book
]
st.write("After Book Value:", len(filtered))

st.subheader("Matching Companies")

st.success(
    f"{len(filtered)} companies match your filters."
)
display_columns = [

    "id",
    "company_name",
    "peer_group_name",
    "return_on_equity_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "operating_profit_margin_pct",
    "interest_coverage",
    "book_value",
    "dividend_payout"

]
st.dataframe(
    filtered[display_columns],
    use_container_width=True,
    hide_index=True
)

