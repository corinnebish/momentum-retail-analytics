import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from statsmodels.tsa.holtwinters import ExponentialSmoothing

st.set_page_config(page_title="Momentum Retail — Strategic Overview", layout="wide", page_icon="📊")

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&display=swap');

html, body, [class*="css"]  {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 15% 10%, rgba(255,110,199,0.18) 0%, transparent 40%),
        radial-gradient(circle at 85% 0%, rgba(125,211,252,0.15) 0%, transparent 35%),
        radial-gradient(circle at 90% 80%, rgba(250,204,21,0.10) 0%, transparent 40%),
        repeating-linear-gradient(45deg, rgba(255,255,255,0.015) 0px, rgba(255,255,255,0.015) 2px, transparent 2px, transparent 6px),
        linear-gradient(160deg, #1e0f3d 0%, #3a1d6e 35%, #6a2c91 70%, #b3417a 100%);
    background-attachment: fixed;
}

.insight-box {
    background: rgba(255,255,255,0.07);
    border-left: 4px solid #facc15;
    border-radius: 8px;
    padding: 12px 16px;
    margin: 8px 0 20px 0;
    font-size: 0.92rem;
    color: #f3ecff;
}
.insight-box b { color: #ffffff; }

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #120829 0%, #241246 100%);
}
section[data-testid="stSidebar"] * {
    color: #f1e8ff !important;
}

h1, h2, h3 {
    color: #ffffff !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px;
}

p, span, label, .stMarkdown {
    color: #e9def7 !important;
}

div[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.18);
    border-radius: 16px;
    padding: 18px 20px 10px 20px;
    backdrop-filter: blur(6px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.25);
}
div[data-testid="stMetricLabel"], div[data-testid="stMetricLabel"] * {
    color: #d9c8ff !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    white-space: normal !important;
    overflow: visible !important;
    text-overflow: unset !important;
}
div[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-weight: 800 !important;
    font-size: 1.35rem !important;
    overflow: visible !important;
    white-space: nowrap !important;
}
div[data-testid="stMetricDelta"] {
    white-space: normal !important;
    overflow: visible !important;
    font-size: 0.8rem !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}
.stTabs [data-baseweb="tab"] {
    background: rgba(255,255,255,0.08);
    border-radius: 10px 10px 0 0;
    color: #e9def7 !important;
    font-weight: 700;
    padding: 10px 20px;
}
.stTabs [aria-selected="true"] {
    background: rgba(255,255,255,0.22) !important;
    color: #ffffff !important;
}

div[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}

hr {
    border-color: rgba(255,255,255,0.15);
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

PLOTLY_TEMPLATE = "plotly_dark"
ACCENT_COLORS = ["#ff6ec7", "#7dd3fc", "#facc15", "#4ade80"]
SEGMENT_COLORS = {
    "Champions": "#4ade80",
    "Loyal Regulars": "#7dd3fc",
    "Average / Occasional": "#facc15",
    "At-Risk Dormant": "#ff6ec7",
}

df = pd.read_excel("Superstore.xlsx", sheet_name="Orders")

SEGMENT_NAMES = {
    2: "Champions",
    3: "Loyal Regulars",
    0: "Average / Occasional",
    1: "At-Risk Dormant",
}

st.title("📊 Momentum Retail — Strategic Overview")
st.caption(
    f"Data covers {df['Order Date'].min().strftime('%b %Y')} "
    f"to {df['Order Date'].max().strftime('%b %Y')}"
)

st.sidebar.header("🔎 Filters")
min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()
date_range = st.sidebar.date_input(
    "Order Date range", value=(min_date, max_date), min_value=min_date, max_value=max_date
)
categories = st.sidebar.multiselect(
    "Category", options=sorted(df["Category"].unique()), default=sorted(df["Category"].unique())
)
regions = st.sidebar.multiselect(
    "Region", options=sorted(df["Region"].unique()), default=sorted(df["Region"].unique())
)

if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

filtered = df[
    (df["Order Date"].dt.date >= start_date)
    & (df["Order Date"].dt.date <= end_date)
    & (df["Category"].isin(categories))
    & (df["Region"].isin(regions))
]

tab1, tab2, tab3 = st.tabs(["📈 Sales Overview", "👥 Customer Segments", "🔮 Revenue Forecast"])

with tab1:
    col1, col2, col3, col4 = st.columns(4)
    total_sales = filtered["Sales"].sum()
    total_orders = filtered["Order ID"].nunique()
    avg_order_value = total_sales / total_orders if total_orders > 0 else 0
    total_profit = filtered["Profit"].sum()
    margin_pct = (total_profit / total_sales * 100) if total_sales > 0 else 0

    col1.metric("💰 Total Sales", f"${total_sales:,.0f}")
    col2.metric("🧾 Total Orders", f"{total_orders:,}")
    col3.metric("📦 Avg Order Value", f"${avg_order_value:,.2f}")
    col4.metric("📈 Profit Margin", f"{margin_pct:.1f}%", f"${total_profit:,.0f} profit")

    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Sales by Category")
        cat_sales = filtered.groupby("Category")["Sales"].sum().sort_values(ascending=False).reset_index()
        fig = px.bar(
            cat_sales, x="Category", y="Sales", color="Category",
            color_discrete_sequence=ACCENT_COLORS, template=PLOTLY_TEMPLATE,
            text_auto=".2s",
        )
        fig.update_layout(
            showlegend=False, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f8f4ff", size=13), xaxis=dict(gridcolor="rgba(255,255,255,0.18)", tickfont=dict(color="#f8f4ff"), title_font=dict(color="#f8f4ff")),
            yaxis=dict(gridcolor="rgba(255,255,255,0.18)", tickfont=dict(color="#f8f4ff"), title_font=dict(color="#f8f4ff")),
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(
            '<div class="insight-box">💡 <b>Furniture</b> sells nearly as much as Technology, '
            'but converts far less of it to profit — heavy discounting is the culprit (see Phase 1 findings).</div>',
            unsafe_allow_html=True,
        )

    with col_b:
        st.subheader("Monthly Sales Over Time")
        monthly = filtered.set_index("Order Date").resample("MS")["Sales"].sum().reset_index()
        fig = px.line(
            monthly, x="Order Date", y="Sales", markers=True,
            color_discrete_sequence=["#7dd3fc"], template=PLOTLY_TEMPLATE,
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f8f4ff", size=13), xaxis=dict(gridcolor="rgba(255,255,255,0.18)", tickfont=dict(color="#f8f4ff"), title_font=dict(color="#f8f4ff")),
            yaxis=dict(gridcolor="rgba(255,255,255,0.18)", tickfont=dict(color="#f8f4ff"), title_font=dict(color="#f8f4ff")),
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(
            '<div class="insight-box">💡 Clear seasonal spikes every <b>Nov-Dec</b> — '
            'the business leans heavily on the holiday period.</div>',
            unsafe_allow_html=True,
        )

    col_c, col_d = st.columns(2)
    with col_c:
        st.subheader("Sales by Region")
        region_sales = filtered.groupby("Region")["Sales"].sum().sort_values(ascending=False).reset_index()
        fig = px.bar(
            region_sales, x="Region", y="Sales", color="Region",
            color_discrete_sequence=ACCENT_COLORS, template=PLOTLY_TEMPLATE, text_auto=".2s",
        )
        fig.update_layout(
            showlegend=False, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f8f4ff", size=13), xaxis=dict(gridcolor="rgba(255,255,255,0.18)", tickfont=dict(color="#f8f4ff"), title_font=dict(color="#f8f4ff")),
            yaxis=dict(gridcolor="rgba(255,255,255,0.18)", tickfont=dict(color="#f8f4ff"), title_font=dict(color="#f8f4ff")),
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(
            '<div class="insight-box">💡 The <b>West</b> and <b>East</b> regions consistently outsell '
            '<b>Central</b> and <b>South</b> — worth checking whether that gap is store count or demand.</div>',
            unsafe_allow_html=True,
        )

    with col_d:
        st.subheader("Discount vs. Profit by Category")
        fig = px.scatter(
            filtered, x="Discount", y="Profit", color="Category",
            color_discrete_sequence=ACCENT_COLORS, template=PLOTLY_TEMPLATE,
            opacity=0.55, trendline="ols", trendline_scope="overall",
        )
        fig.update_traces(marker=dict(size=6))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f8f4ff", size=13), xaxis=dict(gridcolor="rgba(255,255,255,0.18)", tickfont=dict(color="#f8f4ff"), title_font=dict(color="#f8f4ff")),
            yaxis=dict(gridcolor="rgba(255,255,255,0.18)", tickfont=dict(color="#f8f4ff"), title_font=dict(color="#f8f4ff")),
            legend=dict(font=dict(color="#f8f4ff")),
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(
            '<div class="insight-box">💡 Profit drops sharply as discount rises past ~20-40%. '
            '<b>Furniture</b> loses money systemically here (1 in 3 orders, only 2.6% margin), while '
            '<b>Technology</b> has the single worst loss on record (-$6,600 at 70% off) but stays highly '
            'profitable overall (17.4% margin) — an outlier, not a pattern.</div>',
            unsafe_allow_html=True,
        )

with tab2:
    rfm = pd.read_csv("customers_with_clusters.csv")
    rfm["Segment"] = rfm["Cluster"].map(SEGMENT_NAMES)

    st.subheader("Frequency vs. Monetary, by Segment")
    fig = px.scatter(
        rfm, x="Frequency", y="Monetary", color="Segment",
        color_discrete_map=SEGMENT_COLORS, template=PLOTLY_TEMPLATE,
        hover_data=["Customer ID", "Recency"], opacity=0.75,
    )
    fig.update_traces(marker=dict(size=10, line=dict(width=1, color="white")))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f8f4ff", size=13), xaxis=dict(gridcolor="rgba(255,255,255,0.18)", tickfont=dict(color="#f8f4ff"), title_font=dict(color="#f8f4ff")),
        yaxis=dict(gridcolor="rgba(255,255,255,0.18)", tickfont=dict(color="#f8f4ff"), title_font=dict(color="#f8f4ff")),
        legend=dict(font=dict(color="#f8f4ff"), title=dict(font=dict(color="#f8f4ff"))),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(
        '<div class="insight-box">💡 <b>Champions</b> (green) are a small group but spend dramatically '
        'more per relationship — protecting them matters more than growing headcount.</div>',
        unsafe_allow_html=True,
    )

    st.subheader("Average RFM by Segment")
    summary = rfm.groupby("Cluster")[["Recency", "Frequency", "Monetary"]].mean().round(1)
    summary["Segment"] = summary.index.map(SEGMENT_NAMES)
    summary["Customers"] = rfm.groupby("Cluster").size()
    summary = summary[["Segment", "Recency", "Frequency", "Monetary", "Customers"]].reset_index(drop=True)
    st.dataframe(summary, use_container_width=True)

with tab3:
    st.subheader("6-Month Revenue Forecast")
    monthly_full = df.set_index("Order Date").resample("MS")["Sales"].sum()
    model = ExponentialSmoothing(monthly_full, trend="add", seasonal="add", seasonal_periods=12)
    fit = model.fit()
    forecast = fit.forecast(6)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly_full.index, y=monthly_full.values, mode="lines+markers",
        name="Historical Sales", line=dict(color="#7dd3fc", width=3),
    ))
    fig.add_trace(go.Scatter(
        x=forecast.index, y=forecast.values, mode="lines+markers",
        name="6-Month Forecast", line=dict(color="#facc15", width=3, dash="dash"),
    ))
    fig.add_vline(
        x=monthly_full.index[-1], line_width=1.5, line_dash="dot", line_color="rgba(255,255,255,0.5)",
        annotation_text="Forecast starts", annotation_position="top",
        annotation_font=dict(color="#f8f4ff", size=11),
    )
    fig.update_layout(
        template=PLOTLY_TEMPLATE, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f8f4ff", size=13),
        xaxis=dict(gridcolor="rgba(255,255,255,0.18)", tickfont=dict(color="#f8f4ff"), title_font=dict(color="#f8f4ff")), yaxis=dict(gridcolor="rgba(255,255,255,0.18)", tickfont=dict(color="#f8f4ff"), title_font=dict(color="#f8f4ff")),
        xaxis_title="Month", yaxis_title="Total Sales ($)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig, use_container_width=True)

    yearly = df.set_index("Order Date").resample("YS")["Sales"].sum()
    avg_growth = yearly.pct_change().iloc[1:].mean() * 100
    forecast_total = forecast.sum()
    st.markdown(
        f'<div class="insight-box">💡 Revenue has grown <b>~{avg_growth:.0f}%/year</b> on average. '
        f'Next 6 months are projected at <b>${forecast_total:,.0f}</b> total — but the business leans '
        f'heavily on the Nov-Dec peak, so an underperforming holiday season is the key risk to watch.</div>',
        unsafe_allow_html=True,
    )

    st.subheader("Forecasted Values")
    forecast_table = forecast.reset_index()
    forecast_table.columns = ["Month", "Forecasted Sales"]
    forecast_table["Month"] = forecast_table["Month"].dt.strftime("%Y-%m")
    forecast_table["Forecasted Sales"] = forecast_table["Forecasted Sales"].map(lambda x: f"${x:,.2f}")
    st.dataframe(forecast_table, use_container_width=True, hide_index=True)
