import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_excel("Superstore.xlsx", sheet_name="Orders")

# 1. Total Sales by Category
category_sales = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
plt.figure(figsize=(8, 5))
category_sales.plot(kind="barh")
plt.gca().invert_yaxis()
plt.xlabel("Total Sales ($)")
plt.ylabel("Category")
plt.title("Total Sales by Category")
plt.tight_layout()
plt.savefig("category_sales.png")
plt.close()

# 2. Total Sales by Region
region_sales = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
plt.figure(figsize=(8, 5))
region_sales.plot(kind="barh")
plt.gca().invert_yaxis()
plt.xlabel("Total Sales ($)")
plt.ylabel("Region")
plt.title("Total Sales by Region")
plt.tight_layout()
plt.savefig("region_sales.png")
plt.close()

# 3. Monthly total Sales over time
monthly_sales = df.set_index("Order Date").resample("ME")["Sales"].sum()
plt.figure(figsize=(10, 5))
monthly_sales.plot(kind="line")
plt.xlabel("Month")
plt.ylabel("Total Sales ($)")
plt.title("Monthly Total Sales Over Time")
plt.tight_layout()
plt.savefig("monthly_trend.png")
plt.close()

# 4. Discount vs Profit scatter, colored by Category, with trend line
plt.figure(figsize=(8, 6))
categories = df["Category"].unique()
for cat in categories:
    subset = df[df["Category"] == cat]
    plt.scatter(subset["Discount"], subset["Profit"], label=cat, alpha=0.5, s=15)

z = np.polyfit(df["Discount"], df["Profit"], 1)
trend_x = np.linspace(df["Discount"].min(), df["Discount"].max(), 100)
trend_y = np.poly1d(z)(trend_x)
plt.plot(trend_x, trend_y, color="black", linestyle="--", label="Trend line")

plt.xlabel("Discount")
plt.ylabel("Profit ($)")
plt.title("Discount vs. Profit by Category")
plt.legend()
plt.tight_layout()
plt.savefig("discount_profit.png")
plt.close()

print("Saved: category_sales.png, region_sales.png, monthly_trend.png, discount_profit.png")
