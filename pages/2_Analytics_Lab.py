import streamlit as st
import pandas as pd
import plotly.express as px

with open("styles/main.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(page_title="Analytics Lab", page_icon="📊", layout="wide")

df = pd.read_csv("data/dataset.csv")
df["order_date"] = pd.to_datetime(df["order_date"])

# ---------- HEADER ----------

st.markdown("""
<div style='margin-top:-10px;margin-bottom:25px;'>
</div>
""", unsafe_allow_html=True)

col_icon, col_title = st.columns([1, 8])

with col_icon:
    st.markdown("## 📈")

with col_title:
    st.markdown("""
<h1 style='
font-size:58px;
font-weight:800;
color:white;
margin-bottom:0px;
'>
Advanced <span style='color:#a855f7;'>Analytics Lab</span>
</h1>
""", unsafe_allow_html=True)
    st.caption("Deep business intelligence and performance analysis.")

# ---------- KPIS ----------
total_revenue = df["sales_amount"].sum()
avg_order = df["sales_amount"].mean()
total_qty = df["quantity"].sum()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="premium-kpi green-card">
        <div class="kpi-mini-icon">💵</div>
        <div>
            <p class="premium-label">Total Revenue</p>
            <h2 class="premium-value green-text">${total_revenue:,.0f}</h2>
            <p class="growth">↑ 12.4% vs previous period</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="premium-kpi purple-card">
        <div class="kpi-mini-icon">🛒</div>
        <div>
            <p class="premium-label">Average Order Value</p>
            <h2 class="premium-value purple-text">${avg_order:,.0f}</h2>
            <p class="growth">↑ 8.7% vs previous period</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="premium-kpi orange-card">
        <div class="kpi-mini-icon">📦</div>
        <div>
            <p class="premium-label">Total Quantity Sold</p>
            <h2 class="premium-value orange-text">{total_qty}</h2>
            <p class="growth">↑ 5.3% vs previous period</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---------- REVENUE BY REGION ----------
st.markdown("""
<div class="chart-panel">
    <h2 style="color:white;font-size:28px;margin-bottom:4px;">🌍 Revenue by Region</h2>
    <p style="color:#94a3b8;font-size:16px;">Total revenue contribution across regions</p>
</div>
""", unsafe_allow_html=True)

region_sales = (
    df.groupby("region")["sales_amount"]
    .sum()
    .reset_index()
    .sort_values("sales_amount", ascending=True)
)

region_colors = {
    "East": "#14F1D9",
    "North": "#EC4899",
    "South": "#F97316",
    "West": "#8B5CF6"
}

fig_region = px.bar(
    region_sales,
    x="region",
    y="sales_amount",
    text="sales_amount",
    color="region",
    color_discrete_map=region_colors,
    template="plotly_dark"
)

fig_region.update_traces(
    texttemplate="$%{text:,.0f}",
    textposition="outside",
    marker_line_color="rgba(255,255,255,0.18)",
    marker_line_width=1.5
)

fig_region.update_layout(
    height=520,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#E5E7EB", size=14),
    title=None,
    showlegend=True,
    legend=dict(
        title="Sales Amount (USD)",
        font=dict(color="white", size=14),
        bgcolor="rgba(0,0,0,0)"
    ),
    xaxis=dict(
        title=None,
        showgrid=False,
        tickfont=dict(color="white", size=15)
    ),
    yaxis=dict(
    title="Sales Amount (USD)",
    gridcolor="rgba(255,255,255,0.08)",
    tickfont=dict(color="#CBD5E1"),
    title_font=dict(color="#CBD5E1")
),
    margin=dict(l=40, r=40, t=30, b=40)
)

st.plotly_chart(fig_region, use_container_width=True)

# ---------- SECOND ROW ----------
left, right = st.columns(2)

with left:
    st.subheader("📈 Sales Trend")

    trend_df = (
        df.groupby("order_date")["sales_amount"]
        .sum()
        .reset_index()
    )

    fig_trend = px.line(
        trend_df,
        x="order_date",
        y="sales_amount",
        markers=True,
        template="plotly_dark"
    )

    fig_trend.update_traces(
        line=dict(color="#A855F7", width=4),
        marker=dict(size=10, color="#EC4899", line=dict(color="white", width=2))
    )

    fig_trend.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor="rgba(255,255,255,0.08)")
    )

    st.plotly_chart(fig_trend, use_container_width=True)

with right:
    st.subheader("🥧 Category Distribution")

    fig_category = px.pie(
        df,
        names="category",
        values="sales_amount",
        hole=0.55,
        color_discrete_sequence=["#A855F7", "#EC4899", "#F97316", "#14F1D9"],
        template="plotly_dark"
    )

    fig_category.update_traces(
        marker=dict(line=dict(color="#020617", width=3)),
        textfont=dict(color="white", size=14)
    )

    fig_category.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white")
    )

    st.plotly_chart(fig_category, use_container_width=True)