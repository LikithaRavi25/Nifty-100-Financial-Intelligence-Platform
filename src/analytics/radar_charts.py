import sqlite3
import os

import numpy as np
import pandas as pd
from math import pi

import matplotlib.pyplot as plt
from composite_score import composite_quality_score
DATABASE = "nifty100.db"

def load_financial_ratios():

    conn = sqlite3.connect(DATABASE)

    df = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn
    )

    conn.close()

    return df

def load_peer_groups():

    conn = sqlite3.connect(DATABASE)

    peers = pd.read_sql(
        "SELECT * FROM peer_groups",
        conn
    )

    conn.close()

    return peers

def prepare_data():

    ratios = load_financial_ratios()

    peers = load_peer_groups()

    ratios["company_id"] = ratios["company_id"].str.upper()

    peers["company_id"] = peers["company_id"].str.upper()

    merged = ratios.merge(

        peers,

        on="company_id",

        how="left"

    )

    return merged

RADAR_METRICS = [

    "return_on_equity_pct",

    "return_on_capital_employed_pct",

    "net_profit_margin_pct",

    "debt_to_equity",

    "free_cash_flow_cr",

    "pat_cagr_5yr",

    "revenue_cagr_5yr",

    "composite_quality_score"

]


def get_peer_average(data, peer_group):

    peer = data[
        data["peer_group_name"] == peer_group
    ]

    average = peer[
        RADAR_METRICS
    ].mean()

    return average

def create_radar_chart(
    company_name,
    company_values,
    peer_values
):

    labels = RADAR_METRICS

    angles = np.linspace(
        0,
        2 * np.pi,
        len(labels),
        endpoint=False
    ).tolist()

    angles += angles[:1]

    company = company_values.tolist()
    peer = peer_values.tolist()

    company += company[:1]
    peer += peer[:1]

    fig = plt.figure(
        figsize=(8, 8)
    )

    ax = plt.subplot(
        111,
        polar=True
    )

    ax.plot(
        angles,
        company,
        linewidth=2,
        label=company_name
    )

    ax.fill(
        angles,
        company,
        alpha=0.25
    )

    ax.plot(
        angles,
        peer,
        linestyle="--",
        linewidth=2,
        label="Peer Average"
    )

    ax.set_xticks(
        angles[:-1]
    )

    ax.set_xticklabels(
        [
            "ROE",
            "ROCE",
            "NPM",
            "D/E",
            "FCF",
            "PAT CAGR",
            "REV CAGR",
            "Composite"
        ]
    )

    plt.title(
        f"{company_name} Radar Chart"
    )

    plt.legend(
        loc="upper right"
    )

    return fig

def save_radar_chart(company, latest, peer_average):

    os.makedirs(
        "reports/radar_charts",
        exist_ok=True
    )

    fig = create_radar_chart(
        company,
        latest[RADAR_METRICS],
        peer_average
    )

    fig.savefig(
        f"reports/radar_charts/{company}_radar.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close(fig)

    print(f"{company} completed.")


if __name__ == "__main__":

    data = prepare_data()
    print("\nCalculating Composite Score...")

    data["composite_quality_score"] = composite_quality_score(data)


    print(
    data[
        [
            "company_id",
            "composite_quality_score"
        ]
    ].head()
)

    print(data.shape)

    print(data.head())

    print(data.columns.tolist())


    print("\nGenerating Radar Charts...\n")

companies = sorted(
    data["company_id"].unique()
)

for company in companies:

    company_df = data[
        data["company_id"] == company
    ]

    if company_df.empty:
        continue

    latest = company_df.sort_values(
        "year"
    ).iloc[-1]

    if pd.isna(
        latest["peer_group_name"]
    ):
        print(
            f"{company} : No peer group assigned"
        )
        continue

    peer_average = get_peer_average(
        data,
        latest["peer_group_name"]
    )

    save_radar_chart(
        company,
        latest,
        peer_average
    )


    print("\nRadar Chart Saved Successfully!")

    print("\n======================")
    

    print(
    "Charts Generated :",
    len(companies)
)

    print(
    "Location : reports/radar_charts/"
)