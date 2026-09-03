import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

df = pd.read_excel("Superstore.xlsx", sheet_name="Orders")

reference_date = df["Order Date"].max() + pd.Timedelta(days=1)

rfm = df.groupby("Customer ID").agg(
    Recency=("Order Date", lambda x: (reference_date - x.max()).days),
    Frequency=("Order ID", "nunique"),
    Monetary=("Sales", "sum"),
).reset_index()

scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm[["Recency", "Frequency", "Monetary"]])

kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
rfm["Cluster"] = kmeans.fit_predict(rfm_scaled)

print("=== Cluster Summary (Average RFM values) ===")
summary = rfm.groupby("Cluster")[["Recency", "Frequency", "Monetary"]].mean()
summary["Count"] = rfm.groupby("Cluster").size()
print(summary)

plt.figure(figsize=(8, 6))
for cluster in sorted(rfm["Cluster"].unique()):
    subset = rfm[rfm["Cluster"] == cluster]
    plt.scatter(subset["Frequency"], subset["Monetary"], label=f"Cluster {cluster}", alpha=0.6)
plt.xlabel("Frequency (number of orders)")
plt.ylabel("Monetary (total Sales $)")
plt.title("Customer Segments: Frequency vs. Monetary")
plt.legend()
plt.tight_layout()
plt.savefig("rfm_clusters.png")
plt.close()

rfm.to_csv("customers_with_clusters.csv", index=False)
print("\nSaved: rfm_clusters.png, customers_with_clusters.csv")
