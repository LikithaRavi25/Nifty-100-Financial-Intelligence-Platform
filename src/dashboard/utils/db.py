import sqlite3
import pandas as pd
import streamlit as st

DATABASE = "nifty100.db"
@st.cache_data(ttl=600)
def run_query(query, params=None):

    conn = sqlite3.connect(DATABASE)

    if params is None:

        df = pd.read_sql(
            query,
            conn
        )

    else:

        df = pd.read_sql(
            query,
            conn,
            params=params
        )

    conn.close()

    return df

@st.cache_data(ttl=600)
def get_companies():

    return run_query(
        """
        SELECT *
        FROM companies
        ORDER BY company_name
        """
    )

@st.cache_data(ttl=600)
def get_ratios(
    ticker,
    year=None
):

    if year is None:

        query = """
        SELECT *
        FROM financial_ratios
        WHERE company_id=?
        ORDER BY year
        """

        return run_query(
            query,
            [ticker]
        )

    query = """
    SELECT *
    FROM financial_ratios
    WHERE company_id=?
    AND year=?
    """

    return run_query(
        query,
        [ticker, year]
    )

@st.cache_data(ttl=600)
def get_pl(ticker):

    query = """
    SELECT *
    FROM profitandloss
    WHERE company_id=?
    ORDER BY year
    """

    return run_query(
        query,
        [ticker]
    )

@st.cache_data(ttl=600)
def get_bs(ticker):

    query = """
    SELECT *
    FROM balancesheet
    WHERE company_id=?
    ORDER BY year
    """

    return run_query(
        query,
        [ticker]
    )

@st.cache_data(ttl=600)
def get_cf(ticker):

    query = """
    SELECT *
    FROM cashflow
    WHERE company_id=?
    ORDER BY year
    """

    return run_query(
        query,
        [ticker]
    )

@st.cache_data(ttl=600)
def get_sectors():

    query = """
    SELECT *
    FROM sectors
    ORDER BY broad_sector
    """

    return run_query(query)

@st.cache_data(ttl=600)
def get_peers(group_name):

    query = """
    SELECT *
    FROM peer_groups
    WHERE peer_group_name=?
    """

    return run_query(
        query,
        [group_name]
    )

@st.cache_data(ttl=600)
def get_valuation(ticker):
    """
    Placeholder.
    Will be implemented during the valuation module.
    """
    return pd.DataFrame()

@st.cache_data(ttl=600)
def get_home_metrics(year="2024-03"):

    query = """
    SELECT *
    FROM financial_ratios
    WHERE year=?
    """

    return run_query(
        query,
        [year]
    )

@st.cache_data(ttl=600)
def get_sector_distribution():

    query = """
    SELECT
        peer_group_name,
        COUNT(DISTINCT company_id) AS companies
    FROM peer_groups
    GROUP BY peer_group_name
    ORDER BY companies DESC
    """

    return run_query(query)

@st.cache_data(ttl=600)
def get_top_companies(year="2024-03"):

    query = """
    SELECT
        company_id,
        composite_quality_score,
        return_on_equity_pct,
        revenue_cagr_5yr,
        debt_to_equity
    FROM financial_ratios
    WHERE year=?
    ORDER BY composite_quality_score DESC
    LIMIT 5
    """

    return run_query(
        query,
        [year]
    )

@st.cache_data(ttl=600)
def get_company_master():

    query = """
    SELECT
        id,
        company_name
    FROM companies
    ORDER BY company_name
    """

    return run_query(query)

@st.cache_data(ttl=600)
def get_company_details(ticker):

    query = """
    SELECT *
    FROM companies
    WHERE id=?
    """

    return run_query(
        query,
        [ticker]
    )

@st.cache_data(ttl=600)
def get_company_peer_group(ticker):

    query = """
    SELECT peer_group_name
    FROM peer_groups
    WHERE company_id=?
    LIMIT 1
    """

    return run_query(
        query,
        [ticker]
    )

@st.cache_data(ttl=600)
def get_latest_ratios(ticker):

    query = """
    SELECT *
    FROM financial_ratios
    WHERE company_id=?
    ORDER BY year DESC
    LIMIT 1
    """

    return run_query(
        query,
        [ticker]
    )


@st.cache_data(ttl=600)
def get_company_profit_history(ticker):

    query = """
    SELECT
        year,
        sales,
        net_profit
    FROM profitandloss
    WHERE company_id=?
    ORDER BY year
    """

    return run_query(
        query,
        [ticker]
    )

@st.cache_data(ttl=600)
def get_company_ratio_history(ticker):

    query = """
    SELECT
        year,
        return_on_equity_pct,
        return_on_capital_employed_pct
    FROM financial_ratios
    WHERE company_id=?
    ORDER BY year
    """

    return run_query(
        query,
        [ticker]
    )

@st.cache_data(ttl=600)
def get_screener_data():

    query = """
    SELECT
        c.id,
        c.company_name,
        pg.peer_group_name,

        fr.return_on_equity_pct,
        fr.debt_to_equity,
        fr.free_cash_flow_cr,
        fr.revenue_cagr_5yr,
        fr.pat_cagr_5yr,
        fr.operating_profit_margin_pct,
        fr.interest_coverage,
        fr.book_value,
        fr.dividend_payout,

        fr.cfo_quality_score

    FROM financial_ratios fr

    LEFT JOIN companies c

    ON fr.company_id=c.id

    LEFT JOIN peer_groups pg

    ON fr.company_id=pg.company_id

    WHERE fr.year=
    (
        SELECT MAX(year)
        FROM financial_ratios f2
        WHERE f2.company_id=fr.company_id
    )
    """

    return run_query(query)

@st.cache_data(ttl=600)
def get_peer_groups():

    query = """
    SELECT DISTINCT
        peer_group_name
    FROM peer_groups
    ORDER BY peer_group_name
    """

    return run_query(query)

@st.cache_data(ttl=600)
def get_peer_companies(group):

    query = """
    SELECT
        c.id,
        c.company_name

    FROM peer_groups pg

    JOIN companies c
        ON pg.company_id = c.id

    WHERE pg.peer_group_name = ?

    ORDER BY c.company_name
    """

    return run_query(
        query,
        [group]
    )

@st.cache_data(ttl=600)
def get_peer_metrics(group):

    query = """
    SELECT

        fr.company_id,

        c.company_name,

        fr.return_on_equity_pct,
        fr.return_on_capital_employed_pct,
        fr.net_profit_margin_pct,
        fr.operating_profit_margin_pct,
        fr.asset_turnover,
        fr.interest_coverage,
        fr.free_cash_flow_cr,
        fr.debt_to_equity

    FROM financial_ratios fr

    JOIN peer_groups pg
        ON fr.company_id = pg.company_id

    JOIN companies c
        ON fr.company_id = c.id

    WHERE pg.peer_group_name = ?

    AND fr.year =
    (
        SELECT MAX(year)
        FROM financial_ratios f2
        WHERE f2.company_id = fr.company_id
    )
    """

    return run_query(query,[group])

@st.cache_data(ttl=600)
def get_peer_kpi_table(group):

    query = """
    SELECT

        c.company_name,

        fr.return_on_equity_pct,

        fr.return_on_capital_employed_pct,

        fr.net_profit_margin_pct,

        fr.debt_to_equity,

        fr.interest_coverage,

        fr.free_cash_flow_cr,

        pg.is_benchmark

    FROM financial_ratios fr

    JOIN peer_groups pg
        ON fr.company_id = pg.company_id

    JOIN companies c
        ON fr.company_id = c.id

    WHERE pg.peer_group_name = ?

    AND fr.year =
    (
        SELECT MAX(year)
        FROM financial_ratios f2
        WHERE f2.company_id = fr.company_id
    )

    ORDER BY
        fr.return_on_equity_pct DESC
    """

    return run_query(query, [group])

@st.cache_data(ttl=600)
def get_trend_data(ticker):

    query = """
    SELECT

        year,

        sales,

        return_on_equity_pct,

        return_on_capital_employed_pct,

        net_profit_margin_pct,

        operating_profit_margin_pct,

        debt_to_equity,

        free_cash_flow_cr,

        interest_coverage,

        revenue_cagr_5yr,

        pat_cagr_5yr,

        eps_cagr_5yr

    FROM financial_ratios

    WHERE company_id=?

    ORDER BY year
    """

    return run_query(
        query,
        [ticker]
    )

@st.cache_data(ttl=600)
def get_sector_data():

    query = """
    SELECT

        c.company_name,

        s.broad_sector,

        s.sub_sector,

        mc.market_cap_crore,

        fr.sales,

        fr.return_on_equity_pct

    FROM companies c

    JOIN sectors s
        ON c.id = s.company_id

    JOIN financial_ratios fr
        ON c.id = fr.company_id

    JOIN market_cap mc
        ON c.id = mc.company_id

    WHERE fr.year =
    (
        SELECT MAX(year)
        FROM financial_ratios f2
        WHERE f2.company_id = fr.company_id
    )

    AND mc.year =
    (
        SELECT MAX(year)
        FROM market_cap m2
        WHERE m2.company_id = mc.company_id
    )
    """

    return run_query(query)

@st.cache_data(ttl=600)
def get_capital_allocation_data():

    query = """
    SELECT

        c.company_name,

        fr.return_on_equity_pct,

        fr.debt_to_equity,

        fr.free_cash_flow_cr,

        fr.revenue_cagr_5yr,

        fr.pat_cagr_5yr,

        fr.capex_cr,

        fr.dividend_payout,

        mc.market_cap_crore

    FROM financial_ratios fr

    JOIN companies c
        ON fr.company_id = c.id

    JOIN market_cap mc
        ON fr.company_id = mc.company_id

    WHERE fr.year =
    (
        SELECT MAX(year)
        FROM financial_ratios f2
        WHERE f2.company_id = fr.company_id
    )

    AND mc.year =
    (
        SELECT MAX(year)
        FROM market_cap m2
        WHERE m2.company_id = mc.company_id
    )
    """

    return run_query(query)

@st.cache_data(ttl=600)
def get_annual_reports():

    query = """
    SELECT

        c.company_name,

        d.company_id,

        d.year,

        d.annual_report

    FROM documents d

    JOIN companies c

        ON d.company_id = c.id

    ORDER BY
        c.company_name,
        d.year DESC
    """

    return run_query(query)



if __name__ == "__main__":

    print("Companies :", len(get_companies()))

    print("Ratios :", len(get_ratios("TCS")))

    print("P&L :", len(get_pl("TCS")))

    print("Balance Sheet :", len(get_bs("TCS")))

    print("Cash Flow :", len(get_cf("TCS")))

    print("Sectors :", len(get_sectors()))

    print("IT Peers :", len(get_peers("IT Services")))

    print("DB Utility Ready ✅")