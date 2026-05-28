import streamlit as st
import pandas as pd
import plotly.express as px
from ai.llm_service import ask_ai

st.set_page_config(page_title="AI BI Command Center", layout="wide", page_icon="⚡")

with open("styles/main.css", "r") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# ---------------- ULTRA PREMIUM CSS ----------------

# ---------------- DATA ----------------
df = pd.read_csv("data/dataset.csv")
df["order_date"] = pd.to_datetime(df["order_date"])

# ---------------- SIDEBAR ----------------
st.sidebar.markdown("""
<div style='font-family:Space Mono,monospace;font-size:13px;letter-spacing:0.15em;
     color:#00f5ff;text-transform:uppercase;padding:10px 0 18px;
     border-bottom:1px solid rgba(255,255,255,0.08);margin-bottom:18px;'>
⚡ Control Center
</div>
""", unsafe_allow_html=True)

theme = st.sidebar.radio("Theme Mode", ["Dark Neon", "Light Premium"])

# ---------------- LIGHT PREMIUM THEME OVERRIDE ----------------
if theme == "Light Premium":
    st.markdown("""
    <style>
    /* ======= LIGHT PREMIUM FULL OVERRIDE ======= */

    :root {
        --neon-cyan:    #0077cc;
        --neon-violet:  #6c2bd9;
        --neon-pink:    #d4006e;
        --neon-gold:    #c47d00;
        --glass-bg:     rgba(255,255,255,0.72);
        --glass-border: rgba(0,0,0,0.07);
        --text-primary: #0f172a;
        --text-muted:   #64748b;
    }

    /* ---- BACKGROUND ---- */
    .stApp {
        background: #f0f4ff !important;
        background-image:
            radial-gradient(ellipse 80% 60% at 10% 0%,   rgba(0,119,204,0.08)  0%, transparent 55%),
            radial-gradient(ellipse 60% 50% at 92% 8%,   rgba(108,43,217,0.07) 0%, transparent 55%),
            radial-gradient(ellipse 70% 60% at 50% 100%, rgba(212,0,110,0.05)  0%, transparent 55%) !important;
    }

    /* Light subtle grid */
    .stApp::before {
        background-image:
            linear-gradient(rgba(0,119,204,0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0,119,204,0.05) 1px, transparent 1px) !important;
    }

    /* No scanlines on light */
    .stApp::after { display: none !important; }

    /* ---- GLOBAL TEXT ---- */
    html, body, [class*="css"],
    .stMarkdown, .stText, p, span, div,
    label, h1, h2, h3, h4 {
        color: var(--text-primary) !important;
    }

    /* ---- HERO ---- */
    .hero-eyebrow { color: #0077cc !important; }

    .hero-title {
        background: linear-gradient(110deg, #0077cc 0%, #1a1a2e 35%, #6c2bd9 70%, #d4006e 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        filter: none !important;
    }

    .hero-sub { color: #64748b !important; }

    .hero-line {
        background: linear-gradient(90deg, transparent, #0077cc, #6c2bd9, transparent) !important;
    }

    /* ---- KPI CARDS ---- */
    .kpi-card {
        background: rgba(255,255,255,0.85) !important;
        border: 1px solid rgba(0,0,0,0.07) !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06), 0 1px 4px rgba(0,0,0,0.05) !important;
        backdrop-filter: blur(12px) !important;
    }
    .kpi-card:hover {
        box-shadow: 0 12px 40px rgba(0,0,0,0.12), 0 0 20px var(--accent, rgba(0,119,204,0.15)) !important;
    }
    .kpi-card:nth-child(1) { --accent: #0077cc; }
    .kpi-card:nth-child(2) { --accent: #6c2bd9; }
    .kpi-card:nth-child(3) { --accent: #d4006e; }
    .kpi-card:nth-child(4) { --accent: #c47d00; }

    .kpi-label { color: #64748b !important; }
    .kpi-value { text-shadow: none !important; }
    .kpi-badge {
        background: rgba(0,0,0,0.04) !important;
        border: 1px solid rgba(0,0,0,0.08) !important;
        color: #64748b !important;
    }

    /* ---- SECTION HEADER ---- */
    .section-title { color: #0f172a !important; }
    .section-line {
        background: linear-gradient(90deg, rgba(0,0,0,0.10), transparent) !important;
    }

    /* ---- AI INSIGHT ---- */
    .ai-insight-wrap {
        background: linear-gradient(135deg, rgba(0,119,204,0.06), rgba(108,43,217,0.04)) !important;
        border: 1px solid rgba(0,119,204,0.18) !important;
        box-shadow: 0 4px 20px rgba(0,119,204,0.06) !important;
    }
    .ai-tag {
        color: #0077cc !important;
        background: rgba(0,119,204,0.08) !important;
        border: 1px solid rgba(0,119,204,0.18) !important;
    }
    .ai-tag-dot { background: #0077cc !important; }
    .ai-insight-text { color: #1e3a5f !important; }

    /* ---- CHART CARDS ---- */
    .chart-card {
        background: rgba(255,255,255,0.80) !important;
        border-color: rgba(0,0,0,0.07) !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.06) !important;
    }

    /* ---- TEXT INPUT ---- */
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.90) !important;
        border: 1px solid rgba(0,119,204,0.25) !important;
        color: #0f172a !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #0077cc !important;
        box-shadow: 0 0 0 3px rgba(0,119,204,0.12) !important;
    }
    .stTextInput > div > div > input::placeholder { color: #94a3b8 !important; }

    /* ---- AI ANSWER ---- */
    .ai-answer {
        background: linear-gradient(135deg, rgba(108,43,217,0.05), rgba(212,0,110,0.03)) !important;
        border: 1px solid rgba(108,43,217,0.18) !important;
        color: #2d1b69 !important;
    }
    .ai-answer-tag { color: #6c2bd9 !important; }

    /* ---- DOWNLOAD BUTTON ---- */
    .stDownloadButton > button {
        background: linear-gradient(135deg, rgba(0,119,204,0.10), rgba(108,43,217,0.08)) !important;
        border: 1px solid rgba(0,119,204,0.28) !important;
        color: #0077cc !important;
    }
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, rgba(0,119,204,0.18), rgba(108,43,217,0.14)) !important;
        box-shadow: 0 4px 18px rgba(0,119,204,0.18) !important;
    }

    /* ---- SIDEBAR ---- */
    [data-testid="stSidebar"] {
        background: rgba(240,244,255,0.97) !important;
        border-right: 1px solid rgba(0,0,0,0.07) !important;
    }
    [data-testid="stSidebar"] * { color: #0f172a !important; }

    /* ---- DATAFRAME ---- */
    .stDataFrame { border-color: rgba(0,0,0,0.07) !important; }

    /* ---- DIVIDER ---- */
    hr { border-top: 1px solid rgba(0,0,0,0.08) !important; }

    /* ---- FOOTER ---- */
    .footer { color: rgba(100,116,139,0.6) !important; }
    .footer span { color: #0077cc !important; }

    /* ---- DOTS ---- */
    .section-dot { box-shadow: none !important; }

    /* ---- SUCCESS / INFO ---- */
    .stSuccess { background: rgba(0,119,204,0.06) !important; color: #0f172a !important; }
    .stInfo    { background: rgba(108,43,217,0.06) !important; color: #0f172a !important; }

    </style>
    """, unsafe_allow_html=True)

regions = ["All"] + sorted(df["region"].unique().tolist())
selected_region = st.sidebar.selectbox("🌍 Select Region", regions)

min_date = df["order_date"].min()
max_date = df["order_date"].max()
date_range = st.sidebar.date_input("📅 Select Date Range", [min_date, max_date])

filtered_df = df.copy()

if selected_region != "All":
    filtered_df = filtered_df[filtered_df["region"] == selected_region]

if len(date_range) == 2:
    start_date = pd.to_datetime(date_range[0])
    end_date   = pd.to_datetime(date_range[1])
    filtered_df = filtered_df[
        (filtered_df["order_date"] >= start_date) &
        (filtered_df["order_date"] <= end_date)
    ]

# ---------------- HERO HEADER ----------------
st.markdown("""
<div class="hero-wrap">
    <div class="hero-eyebrow">◈ AI-Powered Intelligence Platform ◈</div>
    <div class="hero-title">AI BI Executive<br>Command Center</div>
    <div class="hero-sub">Real-time Smart Insights · KPIs · Interactive Analytics · AI Copilot</div>
    <div class="hero-line"></div>
</div>
""", unsafe_allow_html=True)

# ---------------- KPIs ----------------
total_sales     = filtered_df["sales_amount"].sum()
total_orders    = filtered_df["order_id"].count()
total_quantity  = filtered_df["quantity"].sum()

top_region  = filtered_df.groupby("region")["sales_amount"].sum().idxmax()  if not filtered_df.empty else "N/A"
top_product = filtered_df.groupby("product")["sales_amount"].sum().idxmax() if not filtered_df.empty else "N/A"
avg_order_value = filtered_df["sales_amount"].mean() if not filtered_df.empty else 0

st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi-card">
        <span class="kpi-icon">💰</span>
        <div class="kpi-label">Total Sales</div>
        <div class="kpi-value">${total_sales:,.0f}</div>
        <div class="kpi-badge">Revenue</div>
    </div>
    <div class="kpi-card">
        <span class="kpi-icon">🧾</span>
        <div class="kpi-label">Total Orders</div>
        <div class="kpi-value">{total_orders:,}</div>
        <div class="kpi-badge">Transactions</div>
    </div>
    <div class="kpi-card">
        <span class="kpi-icon">🌍</span>
        <div class="kpi-label">Top Region</div>
        <div class="kpi-value">{top_region}</div>
        <div class="kpi-badge">Best Performer</div>
    </div>
    <div class="kpi-card">
        <span class="kpi-icon">🏆</span>
        <div class="kpi-label">Top Product</div>
        <div class="kpi-value">{top_product}</div>
        <div class="kpi-badge">#1 Product</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='margin:10px 0'></div>", unsafe_allow_html=True)

# ---------------- AI INSIGHT ----------------
st.markdown("""
<div class="section-header">
    <div class="section-dot"></div>
    <div class="section-title">AI Business Insight</div>
    <div class="section-line"></div>
</div>
""", unsafe_allow_html=True)

ai_prompt = f"""
Analyze this sales summary:
Total Sales: {total_sales}
Total Orders: {total_orders}
Top Region: {top_region}
Top Product: {top_product}
Average Order Value: {avg_order_value}

Give a short business insight in simple language.
"""

insight = ask_ai(ai_prompt)

st.markdown(f"""
<div class="ai-insight-wrap">
    <div class="ai-tag"><span class="ai-tag-dot"></span>AI Analysis Active</div>
    <div class="ai-insight-text">{insight}</div>
</div>
""", unsafe_allow_html=True)

# ---------------- CHARTS ROW 1 ----------------
st.markdown("""
<div class="section-header">
    <div class="section-dot" style="background:var(--neon-violet);box-shadow:0 0 10px var(--neon-violet)"></div>
    <div class="section-title">Regional & Category Analysis</div>
    <div class="section-line"></div>
</div>
""", unsafe_allow_html=True)

left, right = st.columns(2, gap="large")

is_light = (theme == "Light Premium")

CHART_CONFIG = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(
        family="DM Sans, sans-serif",
        color="#64748b" if is_light else "#8b9ab5",
        size=12
    ),
    title_font=dict(
        family="Syne, sans-serif",
        color="#0f172a" if is_light else "#f0f4ff",
        size=16
    ),
    margin=dict(l=10, r=10, t=46, b=10),
)

GRID_COLOR = "rgba(0,0,0,0.05)"    if is_light else "rgba(255,255,255,0.04)"
PIE_STROKE = "#f0f4ff"             if is_light else "#020617"
BAR_SCALE1 = [[0,"#e8f0fe"],[0.4,"#0077cc"],[1,"#6c2bd9"]] if is_light else [[0,"#0f2027"],[0.4,"#00f5ff"],[1,"#bf00ff"]]
BAR_SCALE2 = [[0,"#f3e8ff"],[0.5,"#6c2bd9"],[1,"#d4006e"]] if is_light else [[0,"#1a0030"],[0.5,"#bf00ff"],[1,"#ff2d78"]]
PIE_COLORS = ["#0077cc","#6c2bd9","#d4006e","#c47d00","#007a50"] if is_light else ["#00f5ff","#bf00ff","#ff2d78","#ffd700","#00ff88"]
LINE_COLOR = "#0077cc"             if is_light else "#00f5ff"
FILL_COLOR = "rgba(0,119,204,0.07)" if is_light else "rgba(0,245,255,0.05)"
CHART_TMPL = "plotly_white"        if is_light else "plotly_dark"

with left:
    region_sales = filtered_df.groupby("region")["sales_amount"].sum().reset_index()
    fig_region = px.bar(
        region_sales, x="region", y="sales_amount", text="sales_amount",
        title="Revenue by Region",
        color="sales_amount",
        color_continuous_scale=BAR_SCALE1,
        template=CHART_TMPL
    )
    fig_region.update_traces(
        texttemplate="$%{text:,.0f}", textposition="outside",
        marker_line_width=0,
        hovertemplate="<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>"
    )
    fig_region.update_layout(**CHART_CONFIG, coloraxis_showscale=False,
        xaxis=dict(gridcolor=GRID_COLOR),
        yaxis=dict(gridcolor=GRID_COLOR))
    st.plotly_chart(fig_region, use_container_width=True)

with right:
    fig_pie = px.pie(
        filtered_df, names="category", values="sales_amount",
        title="Sales by Category", hole=0.52,
        color_discrete_sequence=PIE_COLORS,
        template=CHART_TMPL
    )
    fig_pie.update_traces(
        textfont=dict(family="Space Mono, monospace", size=11),
        hovertemplate="<b>%{label}</b><br>Sales: $%{value:,.0f}<br>%{percent}<extra></extra>",
        marker=dict(line=dict(color=PIE_STROKE, width=3))
    )
    fig_pie.update_layout(**CHART_CONFIG)
    st.plotly_chart(fig_pie, use_container_width=True)

# ---------------- CHARTS ROW 2 ----------------
st.markdown("""
<div class="section-header">
    <div class="section-dot" style="background:var(--neon-pink);box-shadow:0 0 10px var(--neon-pink)"></div>
    <div class="section-title">Trend & Product Performance</div>
    <div class="section-line"></div>
</div>
""", unsafe_allow_html=True)

left2, right2 = st.columns(2, gap="large")

with left2:
    trend_df = filtered_df.groupby("order_date")["sales_amount"].sum().reset_index()
    fig_trend = px.line(
        trend_df, x="order_date", y="sales_amount", markers=True,
        title="Sales Trend Over Time", template=CHART_TMPL
    )
    marker_stroke = "#f0f4ff" if is_light else "#020617"
    fig_trend.update_traces(
        line=dict(color=LINE_COLOR, width=2.5),
        marker=dict(color=LINE_COLOR, size=6, line=dict(color=marker_stroke, width=2)),
        fill="tozeroy", fillcolor=FILL_COLOR,
        hovertemplate="<b>%{x|%b %d, %Y}</b><br>Sales: $%{y:,.0f}<extra></extra>"
    )
    fig_trend.update_layout(**CHART_CONFIG,
        xaxis=dict(gridcolor=GRID_COLOR),
        yaxis=dict(gridcolor=GRID_COLOR))
    st.plotly_chart(fig_trend, use_container_width=True)

with right2:
    product_df = (
        filtered_df.groupby("product")["sales_amount"].sum()
        .reset_index().sort_values("sales_amount", ascending=False)
    )
    fig_product = px.bar(
        product_df, x="sales_amount", y="product", orientation="h",
        title="Product Performance", template=CHART_TMPL,
        color="sales_amount",
        color_continuous_scale=BAR_SCALE2
    )
    fig_product.update_traces(
        marker_line_width=0,
        hovertemplate="<b>%{y}</b><br>Sales: $%{x:,.0f}<extra></extra>"
    )
    fig_product.update_layout(**CHART_CONFIG, coloraxis_showscale=False,
        xaxis=dict(gridcolor=GRID_COLOR),
        yaxis=dict(gridcolor=GRID_COLOR))
    st.plotly_chart(fig_product, use_container_width=True)

# ---------------- DATA TABLE ----------------
st.markdown("""
<div class="section-header">
    <div class="section-dot" style="background:var(--neon-gold);box-shadow:0 0 10px var(--neon-gold)"></div>
    <div class="section-title">Sales Data Explorer</div>
    <div class="section-line"></div>
</div>
""", unsafe_allow_html=True)

st.dataframe(filtered_df, use_container_width=True)

csv = filtered_df.to_csv(index=False)
st.download_button(
    label="⬇️  EXPORT FILTERED DATA",
    data=csv,
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)

# ---------------- AI CHAT ----------------
st.markdown("""
<div class="section-header" style="margin-top:42px">
    <div class="section-dot"></div>
    <div class="section-title">AI Business Copilot</div>
    <div class="section-line"></div>
</div>
<p style="font-family:'DM Sans',sans-serif;color:{'#64748b' if theme == 'Light Premium' else '#8b9ab5'};font-size:14px;margin:-8px 0 18px;">
Ask anything about your data — trends, forecasts, recommendations.</p>
""", unsafe_allow_html=True)

question = st.text_input("", placeholder="e.g. Which region should I focus on next quarter?")

if question:
    context = f"""
    Dataset columns: {list(df.columns)}
    Filtered data summary:
    Total sales: {total_sales}
    Total orders: {total_orders}
    Top region: {top_region}
    Top product: {top_product}

    User question: {question}
    """
    answer = ask_ai(context)
    st.markdown(f"""
    <div class="ai-answer">
        <div class="ai-answer-tag">◈ Copilot Response</div>
        {answer}
    </div>
    """, unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown("""
<hr>
<div class="footer">
    Built with <span>Python</span> · <span>Streamlit</span> · <span>Pandas</span> · <span>Plotly</span> · <span>AI</span>
</div>
""", unsafe_allow_html=True)