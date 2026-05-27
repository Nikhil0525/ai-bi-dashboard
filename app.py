import streamlit as st
import pandas as pd
import plotly.express as px
from ai.llm_service import ask_ai
from database.queries import get_all_sales

st.set_page_config(page_title="AI BI Command Center", layout="wide", page_icon="⚡")

# ---------------- ULTRA PREMIUM CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --neon-cyan:    #00f5ff;
    --neon-violet:  #bf00ff;
    --neon-pink:    #ff2d78;
    --neon-gold:    #ffd700;
    --glass-bg:     rgba(255,255,255,0.04);
    --glass-border: rgba(255,255,255,0.10);
    --text-primary: #f0f4ff;
    --text-muted:   #8b9ab5;
}

/* ---- ROOT & BACKGROUND ---- */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--text-primary);
}

.stApp {
    background: #020617;
    background-image:
        radial-gradient(ellipse 80% 60% at 10% 0%,   rgba(0,245,255,0.12)  0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 90% 10%,  rgba(191,0,255,0.14)  0%, transparent 55%),
        radial-gradient(ellipse 70% 60% at 50% 100%, rgba(255,45,120,0.10) 0%, transparent 55%);
    min-height: 100vh;
}

/* ---- ANIMATED GRID ---- */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(0,245,255,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,245,255,0.03) 1px, transparent 1px);
    background-size: 60px 60px;
    animation: gridScroll 20s linear infinite;
    pointer-events: none;
    z-index: 0;
}
@keyframes gridScroll {
    0%   { background-position: 0 0; }
    100% { background-position: 60px 60px; }
}

/* ---- SCANLINE OVERLAY ---- */
.stApp::after {
    content: '';
    position: fixed;
    inset: 0;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(0,0,0,0.04) 2px,
        rgba(0,0,0,0.04) 4px
    );
    pointer-events: none;
    z-index: 0;
}

/* ---- HERO TITLE ---- */
.hero-wrap {
    position: relative;
    text-align: center;
    padding: 52px 0 10px;
    overflow: hidden;
}
.hero-eyebrow {
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.35em;
    color: var(--neon-cyan);
    text-transform: uppercase;
    margin-bottom: 14px;
    animation: fadeSlideDown 0.7s ease both;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(36px, 5vw, 68px);
    font-weight: 800;
    line-height: 1.05;
    background: linear-gradient(110deg, var(--neon-cyan) 0%, #ffffff 40%, var(--neon-violet) 75%, var(--neon-pink) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: fadeSlideDown 0.8s ease 0.1s both;
    filter: drop-shadow(0 0 40px rgba(0,245,255,0.25));
}
.hero-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 16px;
    color: var(--text-muted);
    margin-top: 14px;
    letter-spacing: 0.02em;
    animation: fadeSlideDown 0.9s ease 0.2s both;
}
.hero-line {
    width: 120px;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--neon-cyan), var(--neon-violet), transparent);
    margin: 20px auto 0;
    animation: pulseBar 3s ease-in-out infinite;
}
@keyframes pulseBar {
    0%, 100% { opacity: 0.5; width: 120px; }
    50%       { opacity: 1;   width: 220px; }
}
@keyframes fadeSlideDown {
    from { opacity: 0; transform: translateY(-22px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ---- KPI CARDS ---- */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 18px;
    margin: 32px 0 10px;
}
.kpi-card {
    position: relative;
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 20px;
    padding: 28px 24px;
    backdrop-filter: blur(20px);
    overflow: hidden;
    transition: transform 0.35s cubic-bezier(.22,1,.36,1),
                box-shadow  0.35s cubic-bezier(.22,1,.36,1);
    animation: cardEntrance 0.6s cubic-bezier(.22,1,.36,1) both;
}
.kpi-card:nth-child(1) { animation-delay: 0.10s; --accent: var(--neon-cyan);   }
.kpi-card:nth-child(2) { animation-delay: 0.20s; --accent: var(--neon-violet); }
.kpi-card:nth-child(3) { animation-delay: 0.30s; --accent: var(--neon-pink);   }
.kpi-card:nth-child(4) { animation-delay: 0.40s; --accent: var(--neon-gold);   }
@keyframes cardEntrance {
    from { opacity: 0; transform: translateY(30px) scale(0.96); }
    to   { opacity: 1; transform: translateY(0)    scale(1); }
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent), transparent);
    opacity: 0.9;
}
.kpi-card::after {
    content: '';
    position: absolute;
    bottom: -60px; right: -60px;
    width: 130px; height: 130px;
    border-radius: 50%;
    background: radial-gradient(circle, var(--accent) 0%, transparent 70%);
    opacity: 0.08;
    transition: opacity 0.35s;
}
.kpi-card:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 20px 60px rgba(0,0,0,0.5), 0 0 30px var(--accent, rgba(0,245,255,0.2));
    border-color: var(--accent, var(--glass-border));
}
.kpi-card:hover::after { opacity: 0.18; }
.kpi-icon {
    font-size: 22px;
    margin-bottom: 10px;
    display: block;
}
.kpi-label {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 6px;
}
.kpi-value {
    font-family: 'Syne', sans-serif;
    font-size: 30px;
    font-weight: 800;
    color: var(--accent, var(--neon-cyan));
    line-height: 1.1;
    text-shadow: 0 0 20px var(--accent, rgba(0,245,255,0.4));
}
.kpi-badge {
    display: inline-block;
    margin-top: 8px;
    padding: 3px 10px;
    border-radius: 99px;
    font-size: 11px;
    font-family: 'Space Mono', monospace;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.10);
    color: var(--text-muted);
}

/* ---- SECTION HEADER ---- */
.section-header {
    display: flex;
    align-items: center;
    gap: 14px;
    margin: 38px 0 18px;
}
.section-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: var(--neon-cyan);
    box-shadow: 0 0 10px var(--neon-cyan);
    animation: dotPulse 2s ease-in-out infinite;
}
@keyframes dotPulse {
    0%, 100% { transform: scale(1);   opacity: 1;   }
    50%       { transform: scale(1.6); opacity: 0.5; }
}
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.01em;
}
.section-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, var(--glass-border), transparent);
}

/* ---- AI INSIGHT CARD ---- */
.ai-insight-wrap {
    position: relative;
    background: linear-gradient(135deg, rgba(0,245,255,0.06), rgba(191,0,255,0.06));
    border: 1px solid rgba(0,245,255,0.2);
    border-radius: 20px;
    padding: 28px 32px;
    margin-bottom: 10px;
    overflow: hidden;
    animation: fadeSlideDown 0.6s ease 0.3s both;
}
.ai-insight-wrap::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(135deg, transparent 40%, rgba(0,245,255,0.03) 100%);
    pointer-events: none;
}
.ai-tag {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--neon-cyan);
    background: rgba(0,245,255,0.08);
    border: 1px solid rgba(0,245,255,0.2);
    border-radius: 99px;
    padding: 5px 14px;
    margin-bottom: 14px;
}
.ai-tag-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--neon-cyan);
    animation: dotPulse 1.5s ease-in-out infinite;
}
.ai-insight-text {
    font-family: 'DM Sans', sans-serif;
    font-size: 16px;
    line-height: 1.75;
    color: #c8d8f0;
}

/* ---- CHART CARD ---- */
.chart-card {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 20px;
    padding: 24px;
    backdrop-filter: blur(16px);
    transition: border-color 0.3s, box-shadow 0.3s;
}
.chart-card:hover {
    border-color: rgba(0,245,255,0.2);
    box-shadow: 0 10px 40px rgba(0,0,0,0.4);
}

/* ---- DATA TABLE ---- */
.stDataFrame {
    border-radius: 16px !important;
    overflow: hidden !important;
    border: 1px solid var(--glass-border) !important;
}

/* ---- DOWNLOAD BUTTON ---- */
.stDownloadButton > button {
    background: linear-gradient(135deg, rgba(0,245,255,0.12), rgba(191,0,255,0.12)) !important;
    border: 1px solid rgba(0,245,255,0.3) !important;
    color: var(--neon-cyan) !important;
    border-radius: 12px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 12px !important;
    letter-spacing: 0.1em !important;
    padding: 12px 28px !important;
    transition: all 0.3s !important;
}
.stDownloadButton > button:hover {
    background: linear-gradient(135deg, rgba(0,245,255,0.25), rgba(191,0,255,0.25)) !important;
    box-shadow: 0 0 24px rgba(0,245,255,0.25) !important;
    transform: translateY(-2px) !important;
}

/* ---- TEXT INPUT ---- */
/* ---- TEXT INPUT FIX ---- */
.stTextInput input {
    background-color: #0f172a !important;
    color: #ffffff !important;
    border: 1px solid #00f5ff !important;
    border-radius: 14px !important;
    caret-color: #00f5ff !important;
}

.stTextInput input::placeholder {
    color: rgba(255,255,255,0.65) !important;
}

.stTextInput label {
    color: #ffffff !important;
}

[data-testid="stDataFrame"] * {
    color: #111827 !important;
}

.stCodeBlock code {
    color: #00f5ff !important;
}

/* ---- AI ANSWER CARD ---- */
.ai-answer {
    background: linear-gradient(135deg, rgba(191,0,255,0.06), rgba(255,45,120,0.04));
    border: 1px solid rgba(191,0,255,0.2);
    border-radius: 16px;
    padding: 22px 26px;
    font-family: 'DM Sans', sans-serif;
    font-size: 15px;
    line-height: 1.75;
    color: #d0c8f0;
    margin-top: 8px;
    animation: fadeSlideDown 0.4s ease both;
}
.ai-answer-tag {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.25em;
    color: var(--neon-violet);
    text-transform: uppercase;
    margin-bottom: 10px;
}

/* ---- FOOTER ---- */
.footer {
    text-align: center;
    padding: 40px 0 20px;
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.2em;
    color: rgba(139,154,181,0.5);
    text-transform: uppercase;
}
.footer span {
    color: var(--neon-cyan);
    opacity: 0.7;
}

/* ---- SIDEBAR ---- */
[data-testid="stSidebar"] {
    background: rgba(2,6,23,0.95) !important;
    border-right: 1px solid var(--glass-border) !important;
    backdrop-filter: blur(20px) !important;
}
[data-testid="stSidebar"] .stRadio label,
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stDateInput label {
    font-family: 'Space Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: var(--text-muted) !important;
}

/* ---- DIVIDER ---- */
hr {
    border: none !important;
    border-top: 1px solid var(--glass-border) !important;
    margin: 30px 0 !important;
}

/* ---- SUCCESS / INFO STATE ---- */
.stSuccess, .stInfo {
    background: transparent !important;
    border: none !important;
}
</style>
            
""", unsafe_allow_html=True)

# ---------------- DATA ----------------
df = get_all_sales()
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
if theme == "Light Premium":

    st.markdown("""
    <style>

    .stApp {
        background: #f4f7fb !important;
        color: #111827 !important;
    }

    .hero-title {
        -webkit-text-fill-color: #111827 !important;
        color: #111827 !important;
    }

    .hero-sub,
    .section-title,
    .ai-insight-text,
    .footer {
        color: #374151 !important;
    }

    .kpi-card,
    .chart-card,
    .ai-insight-wrap,
    .ai-answer {
        background: rgba(255,255,255,0.85) !important;
        border: 1px solid rgba(0,0,0,0.08) !important;
        color: #111827 !important;
    }

    .stTextInput input {
        background: white !important;
        color: black !important;
    }

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

CHART_CONFIG = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans, sans-serif", color="#8b9ab5", size=12),
    title_font=dict(family="Syne, sans-serif", color="#f0f4ff", size=16),
    margin=dict(l=10, r=10, t=46, b=10),
)

with left:
    region_sales = filtered_df.groupby("region")["sales_amount"].sum().reset_index()
    fig_region = px.bar(
        region_sales, x="region", y="sales_amount", text="sales_amount",
        title="Revenue by Region",
        color="sales_amount",
        color_continuous_scale=[[0,"#0f2027"],[0.4,"#00f5ff"],[1,"#bf00ff"]],
        template="plotly_dark"
    )
    fig_region.update_traces(
        texttemplate="$%{text:,.0f}", textposition="outside",
        marker_line_width=0,
        hovertemplate="<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>"
    )
    fig_region.update_layout(**CHART_CONFIG, coloraxis_showscale=False,
        xaxis=dict(gridcolor="rgba(255,255,255,0.04)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.04)"))
    st.plotly_chart(fig_region, use_container_width=True)

with right:
    fig_pie = px.pie(
        filtered_df, names="category", values="sales_amount",
        title="Sales by Category", hole=0.52,
        color_discrete_sequence=["#00f5ff","#bf00ff","#ff2d78","#ffd700","#00ff88"],
        template="plotly_dark"
    )
    fig_pie.update_traces(
        textfont=dict(family="Space Mono, monospace", size=11),
        hovertemplate="<b>%{label}</b><br>Sales: $%{value:,.0f}<br>%{percent}<extra></extra>",
        marker=dict(line=dict(color="#020617", width=3))
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
        title="Sales Trend Over Time", template="plotly_dark"
    )
    fig_trend.update_traces(
        line=dict(color="#00f5ff", width=2.5),
        marker=dict(color="#00f5ff", size=6, line=dict(color="#020617", width=2)),
        fill="tozeroy", fillcolor="rgba(0,245,255,0.05)",
        hovertemplate="<b>%{x|%b %d, %Y}</b><br>Sales: $%{y:,.0f}<extra></extra>"
    )
    fig_trend.update_layout(**CHART_CONFIG,
        xaxis=dict(gridcolor="rgba(255,255,255,0.04)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.04)"))
    st.plotly_chart(fig_trend, use_container_width=True)

with right2:
    product_df = (
        filtered_df.groupby("product")["sales_amount"].sum()
        .reset_index().sort_values("sales_amount", ascending=False)
    )
    fig_product = px.bar(
        product_df, x="sales_amount", y="product", orientation="h",
        title="Product Performance", template="plotly_dark",
        color="sales_amount",
        color_continuous_scale=[[0,"#1a0030"],[0.5,"#bf00ff"],[1,"#ff2d78"]]
    )
    fig_product.update_traces(
        marker_line_width=0,
        hovertemplate="<b>%{y}</b><br>Sales: $%{x:,.0f}<extra></extra>"
    )
    fig_product.update_layout(**CHART_CONFIG, coloraxis_showscale=False,
        xaxis=dict(gridcolor="rgba(255,255,255,0.04)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.04)"))
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
<p style="font-family:'DM Sans',sans-serif;color:#8b9ab5;font-size:14px;margin:-8px 0 18px;">
Ask anything about your data — trends, forecasts, recommendations.</p>
""", unsafe_allow_html=True)

question = st.text_input("", placeholder="e.g. Which region should I focus on next quarter?")

# ---------------- AI CHAT ----------------
st.markdown("""
<div class="section-header" style="margin-top:42px">
    <div class="section-dot"></div>
    <div class="section-title">AI Business Copilot</div>
    <div class="section-line"></div>
</div>
<p style="font-family:'DM Sans',sans-serif;color:#8b9ab5;font-size:14px;margin:-8px 0 18px;">
Ask anything about your data — trends, forecasts, recommendations.
</p>
""", unsafe_allow_html=True)

question = st.text_input(
    "",
    placeholder="e.g. show sales by region"
)

if question:

    from ai.llm_service import generate_sql_from_question
    from database.connection import run_query

    sql_query = generate_sql_from_question(question)

    st.code(sql_query, language="sql")

    result_df = run_query(sql_query)

    st.dataframe(result_df, use_container_width=True)

# ---------------- FOOTER ----------------
st.markdown("""
<hr>
<div class="footer">
    Built with <span>Python</span> · <span>Streamlit</span> · <span>Pandas</span> · <span>Plotly</span> · <span>AI</span>
</div>
""", unsafe_allow_html=True)