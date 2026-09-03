import pandas as pd

df = pd.read_excel("Superstore.xlsx", sheet_name="Orders")

print("=== Shape ===")
print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

print("\n=== Column Names ===")
for col in df.columns:
    print(f"- {col}")

print("\n=== Order Date Range ===")
print(f"Earliest: {df['Order Date'].min()}")
print(f"Latest:   {df['Order Date'].max()}")

print("\n=== Categories ===")
print(df["Category"].unique())

print("\n=== Sub-Categories ===")
print(df["Sub-Category"].unique())

print(f"\nUnique customers: {df['Customer ID'].nunique()}")

print("\n=== Missing Values Per Column ===")
missing = df.isnull().sum()
print(missing[missing > 0] if missing.sum() > 0 else "No missing values.")

print("\n=== Sales Summary ===")
print(df["Sales"].agg(["min", "max", "mean", "median"]))

print("\n=== Profit Summary ===")
print(df["Profit"].agg(["min", "max", "mean", "median"]))
