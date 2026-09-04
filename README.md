# Momentum Retail — Strategic Overview

**A retail analytics project demonstrating the full data analyst workflow: exploratory analysis, customer segmentation, revenue forecasting, dashboard design, and business storytelling.**

This project uses four years of real-world-style transaction data (the Tableau Sample Superstore dataset — 10,194 orders, 804 customers) to answer three questions leadership actually asks: *What does our customer base look like? Which customers deserve different treatment? Where is revenue heading?*

## Skills Demonstrated

- **Data wrangling & exploratory analysis** — pandas, handling real transactional data (dates, categories, missing values, outliers)
- **Unsupervised machine learning** — RFM feature engineering + K-Means clustering (scikit-learn) to segment customers
- **Time series forecasting** — Holt-Winters exponential smoothing (statsmodels) to project 6 months of revenue
- **Data visualization & dashboard design** — interactive Streamlit dashboard with live filtering (Plotly)
- **Business communication** — translating statistical output into a plain-English recommendation for a non-technical executive audience

## The Business Questions

1. **What does our customer base actually look like?** (exploratory data analysis)
2. **Which customers should we treat differently?** (customer segmentation)
3. **Where is revenue heading over the next six months?** (forecasting)

## Key Findings

- **Furniture is quietly the weakest category.** It sells almost as much as Technology ($755K vs. $840K), but converts far less of it to profit — a 2.6% margin vs. Technology's 17.4%. A third of all Furniture orders lose money outright, driven by discounts above ~20%. This is a discounting problem, not a demand problem.
- **Customers split into four actionable segments** via RFM scoring + K-Means clustering: **Champions** (67 customers, ~$9,450 average spend — protect these relationships), **Loyal Regulars** (294 customers, frequent buyers with room to upsell), **Average/Occasional** (340 customers), and **At-Risk Dormant** (103 customers, no order in ~18 months — win-back opportunity).
- **Revenue has grown ~20-30% year-over-year**, with a sharp, predictable November-December seasonal peak. The 6-month forecast (Jan-Jun 2023) projects ~$364K in revenue — with the caveat that an underperforming holiday season is the single biggest risk to that number.

## How It Was Built

| File | What it does |
|---|---|
| `explore.py`, `explore_charts.py` | Exploratory analysis — data shape, date ranges, missing values, summary stats, and 4 charts (category/region sales, monthly trend, discount-vs-profit) |
| `rfm_segmentation.py` | Scores every customer on Recency/Frequency/Monetary, scales the features, and clusters them into 4 segments with K-Means |
| `forecasting.py` | Fits a Holt-Winters model (trend + 12-month seasonality) and forecasts the next 6 months of revenue |
| `dashboard.py` | Interactive Streamlit dashboard — sidebar filters (date, category, region) driving 3 tabs: Sales Overview, Customer Segments, Revenue Forecast |
| `briefing.txt` | The 5-minute business narrative, written for a non-technical audience — no jargon |
| `customers_with_clusters.csv` | Full segmentation output, one row per customer |

**Tools:** Python, pandas, scikit-learn, statsmodels, Plotly, Streamlit, DuckDB, Claude Code (AI pair-programming assistant — I directed every analytical decision; Claude handled implementation).

## Requirements

- Python 3.12 or newer
- uv for installing and running the project
- Python packages listed in `pyproject.toml`: DuckDB, matplotlib, openpyxl, pandas, Plotly, scikit-learn, seaborn, statsmodels, and Streamlit

## Run the Dashboard

```bash
uv run streamlit run dashboard.py
```
Opens at `http://localhost:8501`.
