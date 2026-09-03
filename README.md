# Momentum Retail — Strategic Overview

An analytics project using the Tableau Sample Superstore dataset (4 years of retail transaction data) to answer three business questions: what does the customer base look like, which customers deserve different treatment, and where is revenue heading?

**Tools:** Python, pandas, scikit-learn, statsmodels, Streamlit, DuckDB, Claude Code.

**What's here:**
- `explore.py` / `explore_charts.py` — exploratory data analysis
- `rfm_segmentation.py` — RFM + K-Means customer segmentation (4 segments)
- `forecasting.py` — Holt-Winters 6-month revenue forecast
- `dashboard.py` — interactive Streamlit dashboard (3 tabs: Sales Overview, Customer Segments, Revenue Forecast)
- `briefing.txt` — 5-minute VP briefing notes
- `customers_with_clusters.csv` — full RFM output per customer

**Run the dashboard:**
```
uv run streamlit run dashboard.py
```

Built as an AI-assisted analyst capstone project, USC MSBA.
