import pandas as pd

df = pd.read_csv("validation_failures.csv")

print("\nTop Issues:\n")
print(df["issue"].value_counts().head(20))