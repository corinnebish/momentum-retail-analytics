# Momentum Retail — Strategic Overview

An end-to-end analytics project built around a fictional retail company, Momentum Retail, using the Tableau **Sample Superstore** dataset — four years (2019-2022) of transaction data covering 10,194 orders across 804 customers, three product categories (Furniture, Office Supplies, Technology), and four US regions.

Playing the role of a data analyst reporting to the VP of Strategy, the project answers three business questions ahead of a quarterly review:

1. **What does our customer base actually look like?**
2. **Which customers should we treat differently?**
3. **Where is revenue heading over the next six months?**

## Tools & Methods

Python, pandas, DuckDB, matplotlib, seaborn, scikit-learn (K-Means clustering), statsmodels (Holt-Winters exponential smoothing), Plotly, Streamlit, and Claude Code as an AI pair-programming assistant.

## Project Structure

| File | Purpose |
|---|---|
| `explore.py` | Loads the Orders sheet and prints shape, date range, categories, missing values, and Sales/Profit summary statistics |
| `explore_charts.py` | Generates 4 EDA charts: Sales by Category, Sales by Region, Monthly Sales trend, Discount vs. Profit scatter |
| `rfm_segmentation.py` | Scores every customer on Recency, Frequency, and Monetary value, scales the features, and runs K-Means (k=4) to produce 4 customer segments |
| `forecasting.py` | Fits a Holt-Winters model (additive trend + seasonality, 12-month cycle) to forecast the next 6 months of revenue |
| `dashboard.py` | Interactive Streamlit dashboard with sidebar filters (date range, category, region) and 3 tabs: Sales Overview, Customer Segments, Revenue Forecast |
| `briefing.txt` | Five-minute verbal briefing notes for the VP, written for a non-technical audience |
| `customers_with_clusters.csv` | Full RFM + cluster assignment output, one row per customer |
| `Superstore.xlsx` | Source data (Orders, People, Returns sheets) |

## Key Findings

- **Furniture is the weakest category despite strong sales.** It generates $754K in sales but only $19.7K in profit (2.6% margin) — a third of all Furniture orders lose money, driven by heavy discounting. Technology and Office Supplies both carry ~17% margins by comparison.
- **Four customer segments emerged from RFM + K-Means:** Champions (67 customers, highest spend by far), Loyal Regulars (294 customers, frequent but lower-spend), Average/Occasional (340 customers), and At-Risk Dormant (103 customers, no order in ~18 months).
- **Revenue has grown ~20-30% year-over-year** with a strong, predictable November-December seasonal peak. The 6-month forecast (Jan-Jun 2023) projects roughly $364K in total revenue.

## Running the Dashboard

```bash
uv run streamlit run dashboard.py
```

Opens at `http://localhost:8501`. Filters in the sidebar (date range, category, region) update the Sales Overview tab live; the Revenue Forecast tab always runs on the full dataset.

## Background

Built as a solo AI-assisted analyst capstone project for USC's MSBA program (Class of Spring 2026), applying methods from DSO 530 (K-Means), DSO 545 (EDA/visualization), DSO 552 (SQL via DuckDB), and GSBA 545 (business storytelling).
