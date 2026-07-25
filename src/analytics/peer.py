import sqlite3
import pandas as pd
import numpy as np
import os


DATABASE = "nifty100.db"
PEER_FILE = "data/raw/peer_groups.xlsx"


def load_financial_ratios():
    """
    Load financial ratios from SQLite.
    """

    conn = sqlite3.connect(DATABASE)

    ratios = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn
    )

    conn.close()

    return ratios


def load_peer_groups():
    """
    Load peer groups from Excel.
    """

    peers = pd.read_excel(PEER_FILE)

    peers["company_id"] = (
        peers["company_id"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    return peers


def prepare_ratios(df):
    """
    Standardize company ids.
    """

    df = df.copy()

    df["company_id"] = (
        df["company_id"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    return df


def merge_peer_groups(
    ratios,
    peers
):
    """
    Merge financial ratios with peer groups.
    """

    merged = ratios.merge(

        peers[
            [
                "company_id",
                "peer_group_name",
                "is_benchmark"
            ]
        ],

        on="company_id",

        how="left"

    )

    return merged


def validate_peer_groups(df):
    """
    Print merge statistics.
    """

    print("\n==============================")
    print("PEER GROUP VALIDATION")
    print("==============================")

    print("Rows :", len(df))

    print(
        "Companies without peer group :",
        df["peer_group_name"].isna().sum()
    )

    print()

    print(
        df[
            [
                "company_id",
                "year",
                "peer_group_name",
                "is_benchmark"
            ]
        ].head(15)
    )
METRICS = {
    "return_on_equity_pct": False,
    "return_on_capital_employed_pct": False,
    "net_profit_margin_pct": False,
    "free_cash_flow_cr": False,
    "revenue_cagr_5yr": False,
    "pat_cagr_5yr": False,
    "eps_cagr_5yr": False,
    "interest_coverage": False,
    "asset_turnover": False,
    "debt_to_equity": True
}

def calculate_percentile(group, metric, reverse=False):
    """
    Calculate percentile rank for a metric.
    """

    temp = group.copy()

    if reverse:

        temp["percentile_rank"] = (
            1 - temp[metric].rank(pct=True)
        ) * 100

    else:

        temp["percentile_rank"] = (
            temp[metric].rank(pct=True)
        ) * 100

    temp["percentile_rank"] = (
        temp["percentile_rank"]
        .round(2)
    )

    return temp

def generate_peer_rankings(df):

    results = []

    for metric, reverse in METRICS.items():

        print(f"Ranking {metric}...")

        groups = df.groupby("peer_group_name")

        for peer_name, group in groups:

            ranked = calculate_percentile(
                group,
                metric,
                reverse
            )

            ranked["metric"] = metric

            ranked["value"] = ranked[metric]

            results.append(

                ranked[
                    [
                        "company_id",
                        "year",
                        "peer_group_name",
                        "metric",
                        "value",
                        "percentile_rank"
                    ]
                ]

            )

    return pd.concat(
        results,
        ignore_index=True
    )

def save_peer_percentiles(df):
    """
    Save peer percentile rankings to SQLite.
    """

    conn = sqlite3.connect(DATABASE)

    df.to_sql(
        "peer_percentiles",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()

    print("\npeer_percentiles table saved successfully.")


def export_peer_rankings(df):
    """
    Export peer rankings to Excel.
    """

    os.makedirs("output", exist_ok=True)

    output_file = "output/peer_comparison.xlsx"

    df.to_excel(
        output_file,
        index=False
    )

    print(f"\nExcel exported to: {output_file}")


def verify_results(df):
    """
    Verify generated rankings.
    """

    print("\n==============================")
    print("VERIFICATION")
    print("==============================")

    print("Total Rows :", len(df))

    print("Unique Companies :",
          df["company_id"].nunique())

    print("Unique Peer Groups :",
          df["peer_group_name"].nunique())

    print("Metrics Ranked :",
          df["metric"].nunique())

    print("\nSample Output\n")

    print(df.head(20))

if __name__ == "__main__":

    print("\nLoading Financial Ratios...")

    ratios = load_financial_ratios()

    ratios = prepare_ratios(ratios)

    print(ratios.shape)

    print("\nLoading Peer Groups...")

    peers = load_peer_groups()

    print(peers.shape)

    print("\nFiltering Peer Universe...")

    ratios = ratios[
        ratios["company_id"].isin(
            peers["company_id"]
        )
    ]

    print(ratios.shape)

    print("\nMerging...")

    merged = merge_peer_groups(
        ratios,
        peers
    )

    validate_peer_groups(
        merged
    )

    print("\nGenerating Peer Percentiles...\n")

    peer_percentiles = generate_peer_rankings(
    merged
)

    print(peer_percentiles.head())
    print()

    print("Total percentile rows:")

    print(len(peer_percentiles))

    save_peer_percentiles(
    peer_percentiles
)

    export_peer_rankings(
    peer_percentiles
)

    verify_results(
    peer_percentiles
)