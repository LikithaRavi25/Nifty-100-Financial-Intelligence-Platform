import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path

from sklearn.cluster import KMeans

from sklearn.preprocessing import StandardScaler

from scipy.spatial.distance import cdist

BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "nifty100.db"

OUTPUT_DIR = BASE_DIR / "output"

REPORT_DIR = OUTPUT_DIR / "reports"

OUTPUT_DIR.mkdir(exist_ok=True)

REPORT_DIR.mkdir(exist_ok=True)
conn = sqlite3.connect(DB_PATH)

query = """

SELECT

fr.company_id,

s.broad_sector,

fr.return_on_equity_pct,

fr.debt_to_equity,

fr.sales,

fr.free_cash_flow_cr,

fr.operating_profit_margin_pct

FROM financial_ratios fr

LEFT JOIN sectors s

ON fr.company_id = s.company_id

WHERE fr.year = (

    SELECT MAX(year)

    FROM financial_ratios f2

    WHERE f2.company_id = fr.company_id

)

ORDER BY fr.company_id

"""

df = pd.read_sql(query, conn)

print(df.shape)

print(df.head())

print(df.columns.tolist())

print("\nMissing Values")

print(df.isnull().sum())

# Fill missing sectors

df["broad_sector"] = df["broad_sector"].fillna("Unknown")

features = [
    "return_on_equity_pct",
    "debt_to_equity",
    "sales",
    "free_cash_flow_cr",
    "operating_profit_margin_pct"
]

for column in features:

    df[column] = (

        df
        .groupby("broad_sector")[column]
        .transform(
            lambda x: x.fillna(x.median())
        )

    )

    df[features] = df[features].fillna(

    df[features].median()

)
    print("\nAfter Imputation")

    print(df[features].isnull().sum())

    X = df[features]

    print(X.head())
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    scaled_df = pd.DataFrame(
    X_scaled,
    columns=features
)
    print("\nScaled Data")

    print(scaled_df.head())
    print("\nMeans")

    print(scaled_df.mean())
    print("\nStandard Deviations")

    print(scaled_df.std())
    # ---------------------------------------------------
# Elbow Method
# ---------------------------------------------------

inertia = []
for k in range(2, 11):

    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    model.fit(X_scaled)

    inertia.append(model.inertia_)
    print("\nInertia Values")

for k, value in zip(range(2, 11), inertia):

    print(f"k = {k} : {value:.2f}")
    plt.figure(figsize=(7,5))

    plt.plot(
    range(2,11),
    inertia,
    marker="o",
    linewidth=2
)

    plt.title("Elbow Method")

    plt.xlabel("Number of Clusters (k)")
    plt.ylabel("Inertia")

    plt.grid(True)

    plt.tight_layout()
    plt.savefig(
    REPORT_DIR / "elbow_plot.png",
    dpi=300
)

    plt.close()

    print("✅ elbow_plot.png saved")

# ---------------------------------------------------
# Final KMeans Model
# ---------------------------------------------------

kmeans = KMeans(
    n_clusters=5,
    random_state=42,
    n_init=10
)

kmeans.fit(X_scaled)
df["cluster_id"] = kmeans.labels_
print(df[
    [
        "company_id",
        "cluster_id"
    ]
].head(10))
print("\nCluster Distribution")

print(
    df["cluster_id"]
    .value_counts()
    .sort_index()
)
cluster_names = {

    0: "Quality Compounders",

    1: "Growth Leaders",

    2: "Value Opportunities",

    3: "High Leverage",

    4: "Turnaround Candidates"

}
df["cluster_name"] = (
    df["cluster_id"]
    .map(cluster_names)
)
print(

    df[
        [
            "company_id",
            "cluster_id",
            "cluster_name"
        ]
    ].head(10)

)
print("\nCluster Summary")

print(

    df.groupby("cluster_name")
      .size()

)
# ---------------------------------------------------
# Distance from Cluster Centroid
# ---------------------------------------------------

distances = cdist(
    X_scaled,
    kmeans.cluster_centers_,
    metric="euclidean"
)

df["distance_from_centroid"] = distances.min(axis=1)
print(df[
    [
        "company_id",
        "cluster_name",
        "distance_from_centroid"
    ]
].head(10))
cluster_output = df[
    [
        "company_id",
        "cluster_id",
        "cluster_name",
        "distance_from_centroid"
    ]
]
cluster_output.to_csv(
    OUTPUT_DIR / "cluster_labels.csv",
    index=False
)

print("✅ cluster_labels.csv saved")
print("\nCompanies Clustered :", len(cluster_output))
print("\nUnique Clusters")

print(sorted(df["cluster_id"].unique()))
print("\nCluster Names")

print(df["cluster_name"].unique())
print("\n====================================")
print("KMeans Clustering Completed")
print("====================================")

print("Companies :", len(cluster_output))
print("Clusters :", df["cluster_id"].nunique())

print("\nOutput File : cluster_labels.csv")
print("Elbow Plot : reports/elbow_plot.png")