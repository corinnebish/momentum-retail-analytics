import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing

df = pd.read_excel("Superstore.xlsx", sheet_name="Orders")

monthly_sales = df.set_index("Order Date").resample("MS")["Sales"].sum()

plt.figure(figsize=(10, 5))
monthly_sales.plot(kind="line")
plt.xlabel("Month")
plt.ylabel("Total Sales ($)")
plt.title("Historical Monthly Sales")
plt.tight_layout()
plt.savefig("historical_sales.png")
plt.close()

model = ExponentialSmoothing(
    monthly_sales, trend="add", seasonal="add", seasonal_periods=12
)
fit = model.fit()
forecast = fit.forecast(6)

plt.figure(figsize=(10, 5))
plt.plot(monthly_sales.index, monthly_sales.values, color="blue", linestyle="-", label="Historical Sales")
plt.plot(forecast.index, forecast.values, color="orange", linestyle="--", label="6-Month Forecast")
plt.xlabel("Month")
plt.ylabel("Total Sales ($)")
plt.title("Monthly Sales: Historical + 6-Month Forecast")
plt.legend()
plt.tight_layout()
plt.savefig("forecast.png")
plt.close()

print("=== 6-Month Forecast ===")
for month, value in forecast.items():
    print(f"{month.strftime('%Y-%m')}: ${value:,.2f}")

print("\nSaved: historical_sales.png, forecast.png")
