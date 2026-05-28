import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Analytics Lab", page_icon="📊", layout="wide")

# ============================================================
#  PREMIUM CSS  —  same design language as Command Center
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --cyan:        #00f5ff;
    --violet:      #bf00ff;
    --pink:        #ff2d78;
    --gold:        #ffd700;
    --green:       #00e5a0;
    --orange:      #ff7b2c;
    --glass-bg:    rgba(255,255,255,0.04);
    --glass-bdr:   rgba(255,255,255,0.10);
    --txt:         #f0f4ff;
    --muted:       #8b9ab5;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--txt);
}

/* ── DEEP SPACE BACKGROUND ── */
.stApp {
    background: #020617;
    background-image:
        radial-gradient(ellipse 80% 55% at 8%  0%,   rgba(0,245,255,0.11) 0%, transparent 58%),
        radial-gradient(ellipse 55% 50% at 92% 5%,   rgba(191,0,255,0.13) 0%, transparent 54%),
        radial-gradient(ellipse 65% 55% at 50% 100%,  rgba(255,45,120,0.09) 0%, transparent 55%);
    min-height: 100vh;
}

/* ── ANIMATED GRID ── */
.stApp::before {
    content:'';
    position:fixed;
    inset:0;
    background-image:
        linear-gradient(rgba(0,245,255,0.028) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,245,255,0.028) 1px, transparent 1px);
    background-size:60px 60px;
    animation: gridScroll 22s linear infinite;
    pointer-events:none;
    z-index:0;
}
@keyframes gridScroll {
    0%   { background-position:0 0; }
    100% { background-position:60px 60px; }
}

/* ── SCANLINES ── */
.stApp::after {
    content:'';
    position:fixed;
    inset:0;
    background: repeating-linear-gradient(
        0deg, transparent, transparent 2px,
        rgba(0,0,0,0.04) 2px, rgba(0,0,0,0.04) 4px
    );
    pointer-events:none;
    z-index:0;
}

/* ── PAGE HEADER ── */
.lab-hero {
    padding: 42px 0 8px;
    display: flex;
    align-items: center;
    gap: 22px;
    animation: fadeDown .7s cubic-bezier(.22,1,.36,1) both;
}
.lab-hero-icon {
    width: 72px; height: 72px;
    border-radius: 18px;
    background: linear-gradient(135deg, rgba(168,85,247,0.25), rgba(191,0,255,0.18));
    border: 1px solid rgba(168,85,247,0.35);
    display: flex; align-items: center; justify-content: center;
    font-size: 34px;
    box-shadow: 0 0 28px rgba(168,85,247,0.2);
    flex-shrink: 0;
}
.lab-hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(32px, 4vw, 58px);
    font-weight: 800;
    line-height: 1.05;
    color: #f0f4ff;
    margin: 0;
}
.lab-hero-title span {
    background: linear-gradient(90deg, #a855f7, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.lab-hero-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 15px;
    color: var(--muted);
    margin-top: 5px;
}
@keyframes fadeDown {
    from { opacity:0; transform:translateY(-20px); }
    to   { opacity:1; transform:translateY(0); }
}

/* ── DATE BADGE ── */
.date-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-family: 'Space Mono', monospace;
    font-size: 12px;
    color: var(--txt);
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 10px;
    padding: 8px 16px;
    letter-spacing: 0.05em;
}

/* ── KPI CARDS ── */
.kpi-row {
    display: grid;
    grid-template-columns: repeat(3,1fr);
    gap: 18px;
    margin: 28px 0 10px;
}
.kpi-lab {
    position: relative;
    border-radius: 20px;
    padding: 26px 24px;
    background: var(--glass-bg);
    border: 1px solid var(--glass-bdr);
    backdrop-filter: blur(18px);
    overflow: hidden;
    display: flex;
    align-items: flex-start;
    gap: 18px;
    transition: transform .35s cubic-bezier(.22,1,.36,1), box-shadow .35s;
    animation: cardUp .6s cubic-bezier(.22,1,.36,1) both;
}
.kpi-lab:nth-child(1) { animation-delay:.10s; --ka:#00e5a0; }
.kpi-lab:nth-child(2) { animation-delay:.20s; --ka:#a855f7; }
.kpi-lab:nth-child(3) { animation-delay:.30s; --ka:#ff7b2c; }
@keyframes cardUp {
    from { opacity:0; transform:translateY(28px) scale(.97); }
    to   { opacity:1; transform:translateY(0)    scale(1); }
}
.kpi-lab::before {
    content:'';
    position:absolute;
    top:0; left:0; right:0;
    height:2px;
    background:linear-gradient(90deg, transparent, var(--ka), transparent);
}
.kpi-lab::after {
    content:'';
    position:absolute;
    bottom:-55px; right:-55px;
    width:120px; height:120px;
    border-radius:50%;
    background:radial-gradient(circle, var(--ka) 0%, transparent 70%);
    opacity:.08;
    transition:opacity .3s;
}
.kpi-lab:hover { transform:translateY(-7px) scale(1.015); box-shadow:0 20px 55px rgba(0,0,0,.5), 0 0 28px var(--ka); border-color:var(--ka); }
.kpi-lab:hover::after { opacity:.18; }

.kpi-icon-box {
    width:52px; height:52px;
    border-radius:14px;
    display:flex; align-items:center; justify-content:center;
    font-size:24px;
    flex-shrink:0;
    border:1px solid rgba(255,255,255,0.1);
}
.kpi-green-box  { background:linear-gradient(135deg,rgba(0,229,160,.18),rgba(0,229,160,.08)); }
.kpi-purple-box { background:linear-gradient(135deg,rgba(168,85,247,.18),rgba(168,85,247,.08)); }
.kpi-orange-box { background:linear-gradient(135deg,rgba(255,123,44,.18),rgba(255,123,44,.08)); }

.kpi-lab-label {
    font-family:'Space Mono',monospace;
    font-size:10px;
    letter-spacing:.22em;
    text-transform:uppercase;
    color:var(--muted);
    margin-bottom:4px;
}
.kpi-lab-value {
    font-family:'Syne',sans-serif;
    font-size:34px;
    font-weight:800;
    line-height:1.1;
    color:var(--ka);
    text-shadow:0 0 22px var(--ka);
    margin-bottom:6px;
}
.kpi-growth {
    font-family:'DM Sans',sans-serif;
    font-size:13px;
    color:#22c55e;
    display:flex;
    align-items:center;
    gap:4px;
}
.kpi-growth::before { content:'↑'; font-weight:700; }

/* ── SECTION HEADERS ── */
.section-hdr {
    display:flex;
    align-items:center;
    gap:13px;
    margin:36px 0 16px;
}
.section-dot {
    width:8px; height:8px;
    border-radius:50%;
    animation:dotPulse 2s ease-in-out infinite;
}
@keyframes dotPulse {
    0%,100%{ transform:scale(1);   opacity:1; }
    50%    { transform:scale(1.6); opacity:.5; }
}
.section-hdr-text { font-family:'Syne',sans-serif; font-size:22px; font-weight:700; color:var(--txt); }
.section-hdr-sub  { font-family:'DM Sans',sans-serif; font-size:14px; color:var(--muted); margin-top:-12px; margin-bottom:16px; margin-left:21px; }
.section-line { flex:1; height:1px; background:linear-gradient(90deg,var(--glass-bdr),transparent); }

/* ── CHART WRAPPER ── */
.chart-wrap {
    background:var(--glass-bg);
    border:1px solid var(--glass-bdr);
    border-radius:20px;
    padding:6px 0;
    backdrop-filter:blur(14px);
    transition:border-color .3s, box-shadow .3s;
}
.chart-wrap:hover {
    border-color:rgba(0,245,255,.18);
    box-shadow:0 10px 40px rgba(0,0,0,.4);
}

/* ── REGION SECTION LABEL ── */
.region-section-icon {
    display:inline-flex;
    align-items:center;
    gap:10px;
    font-family:'Syne',sans-serif;
    font-size:22px;
    font-weight:700;
    color:var(--txt);
}

/* ── FOOTER ── */
.lab-footer {
    text-align:center;
    padding:36px 0 18px;
    font-family:'Space Mono',monospace;
    font-size:11px;
    letter-spacing:.2em;
    color:rgba(139,154,181,.45);
    text-transform:uppercase;
}
.lab-footer span { color:var(--cyan); opacity:.75; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background:rgba(2,6,23,.97) !important;
    border-right:1px solid var(--glass-bdr) !important;
}

hr {
    border:none !important;
    border-top:1px solid var(--glass-bdr) !important;
    margin:28px 0 !important;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
#  DATA
# ============================================================
df = pd.read_csv("data/dataset.csv")
df["order_date"] = pd.to_datetime(df["order_date"])

# ============================================================
#  SHARED CHART CONFIG
# ============================================================
CHART_CFG = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans, sans-serif", color="#8b9ab5", size=13),
    title_font=dict(family="Syne, sans-serif", color="#f0f4ff", size=16),
    margin=dict(l=10, r=10, t=46, b=10),
)
GRID = "rgba(255,255,255,0.05)"

# ============================================================
#  SIDEBAR
# ============================================================
st.sidebar.markdown("""
<div style='font-family:Space Mono,monospace;font-size:13px;letter-spacing:.15em;
     color:#00f5ff;text-transform:uppercase;padding:10px 0 16px;
     border-bottom:1px solid rgba(255,255,255,0.08);margin-bottom:16px;'>
📊 Analytics Lab
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<div style='font-family:Space Mono,monospace;font-size:10px;letter-spacing:.18em;
     color:#8b9ab5;text-transform:uppercase;margin-bottom:8px;'>Navigation</div>
""", unsafe_allow_html=True)

pages = {
    "🏠 Executive Overview":  "executive_overview",
    "📊 Analytics Lab":       "analytics_lab",
    "🤖 AI SQL Copilot":      "sql_copilot",
    "🗄️ Data Explorer":       "data_explorer",
}
for label in pages:
    active = "analytics_lab" in pages[label]
    bg    = "rgba(168,85,247,0.18)"  if active else "transparent"
    bdr   = "rgba(168,85,247,0.5)"   if active else "transparent"
    color = "#a855f7"                if active else "#8b9ab5"
    fw    = "700"                    if active else "400"
    st.sidebar.markdown(f"""
    <div style='display:flex;align-items:center;gap:10px;padding:10px 14px;border-radius:12px;
         background:{bg};border:1px solid {bdr};margin-bottom:6px;cursor:pointer;
         font-family:DM Sans,sans-serif;font-size:14px;font-weight:{fw};color:{color};'>
        {label}
    </div>""", unsafe_allow_html=True)

# ============================================================
#  HEADER
# ============================================================
top_left, top_right = st.columns([6, 1])

with top_left:
    st.markdown("""
    <div class="lab-hero">
        <div class="lab-hero-icon">📈</div>
        <div>
            <div class="lab-hero-title">Advanced <span>Analytics Lab</span></div>
            <div class="lab-hero-sub">Deep business intelligence and performance analysis.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with top_right:
    st.markdown("<div style='padding-top:48px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="date-badge">
        📅 Last 30 Days &nbsp;▾
    </div>
    """, unsafe_allow_html=True)

# ============================================================
#  KPIs
# ============================================================
total_revenue = df["sales_amount"].sum()
avg_order     = df["sales_amount"].mean()
total_qty     = df["quantity"].sum()

st.markdown(f"""
<div class="kpi-row">

  <div class="kpi-lab">
    <div class="kpi-icon-box kpi-green-box">💵</div>
    <div>
      <div class="kpi-lab-label">Total Revenue</div>
      <div class="kpi-lab-value">${total_revenue:,.0f}</div>
      <div class="kpi-growth">12.4% vs previous period</div>
    </div>
  </div>

  <div class="kpi-lab">
    <div class="kpi-icon-box kpi-purple-box">🛒</div>
    <div>
      <div class="kpi-lab-label">Average Order Value</div>
      <div class="kpi-lab-value">${avg_order:,.0f}</div>
      <div class="kpi-growth">8.7% vs previous period</div>
    </div>
  </div>

  <div class="kpi-lab">
    <div class="kpi-icon-box kpi-orange-box">📦</div>
    <div>
      <div class="kpi-lab-label">Total Quantity Sold</div>
      <div class="kpi-lab-value">{total_qty:,}</div>
      <div class="kpi-growth">5.3% vs previous period</div>
    </div>
  </div>

</div>
""", unsafe_allow_html=True)

# ============================================================
#  REVENUE BY REGION
# ============================================================
st.markdown("""
<div class="section-hdr">
    <div class="section-dot" style="background:#00f5ff;box-shadow:0 0 10px #00f5ff;"></div>
    <div class="section-hdr-text">🌍 Revenue by Region</div>
    <div class="section-line"></div>
</div>
<div class="section-hdr-sub">Total revenue contribution across regions</div>
""", unsafe_allow_html=True)

region_sales = (
    df.groupby("region")["sales_amount"]
    .sum().reset_index()
    .sort_values("sales_amount", ascending=True)
)

REGION_COLORS = {
    "East":    "#14F1D9",
    "North":   "#EC4899",
    "South":   "#F97316",
    "West":    "#8B5CF6",
    "Central": "#a855f7",
}

fig_region = px.bar(
    region_sales,
    x="region", y="sales_amount", text="sales_amount",
    color="region",
    color_discrete_map=REGION_COLORS,
    template="plotly_dark"
)
fig_region.update_traces(
    texttemplate="$%{text:,.0f}", textposition="outside",
    marker_line_color="rgba(255,255,255,0.15)",
    marker_line_width=1.5,
    hovertemplate="<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>"
)
fig_region.update_layout(
    **CHART_CFG,
    height=500,
    showlegend=True,
    legend=dict(
        title=dict(text="Region", font=dict(color="#8b9ab5", size=12)),
        font=dict(color="#f0f4ff", size=13),
        bgcolor="rgba(0,0,0,0)",
        bordercolor="rgba(255,255,255,0.08)",
        borderwidth=1,
    ),
    xaxis=dict(
        title=None, showgrid=False,
        tickfont=dict(color="#f0f4ff", size=14, family="DM Sans, sans-serif"),
        zeroline=False,
    ),
    yaxis=dict(
        title=dict(text="Sales Amount (USD)", font=dict(color="#8b9ab5", size=13)),
        gridcolor=GRID,
        tickfont=dict(color="#8b9ab5"),
        zeroline=False,
    ),
)
st.plotly_chart(fig_region, use_container_width=True)

# ============================================================
#  SALES TREND  +  CATEGORY PIE
# ============================================================
st.markdown("""
<div class="section-hdr">
    <div class="section-dot" style="background:#bf00ff;box-shadow:0 0 10px #bf00ff;"></div>
    <div class="section-hdr-text">Trend & Distribution</div>
    <div class="section-line"></div>
</div>
""", unsafe_allow_html=True)

col_trend, col_pie = st.columns(2, gap="large")

with col_trend:
    st.markdown("""
    <div style='font-family:Syne,sans-serif;font-size:18px;font-weight:700;
         color:#f0f4ff;margin-bottom:4px;'>📈 Sales Trend</div>
    <div style='font-family:DM Sans,sans-serif;font-size:13px;color:#8b9ab5;
         margin-bottom:12px;'>Revenue over time</div>
    """, unsafe_allow_html=True)

    trend_df = (
        df.groupby("order_date")["sales_amount"]
        .sum().reset_index()
    )
    fig_trend = px.line(
        trend_df, x="order_date", y="sales_amount",
        markers=True, template="plotly_dark"
    )
    fig_trend.update_traces(
        line=dict(color="#a855f7", width=3.5),
        marker=dict(size=9, color="#ec4899",
                    line=dict(color="#020617", width=2)),
        fill="tozeroy",
        fillcolor="rgba(168,85,247,0.07)",
        hovertemplate="<b>%{x|%b %d, %Y}</b><br>$%{y:,.0f}<extra></extra>"
    )
    fig_trend.update_layout(
        **CHART_CFG,
        height=380,
        xaxis=dict(showgrid=False, tickfont=dict(color="#8b9ab5"),
                   title=None, zeroline=False),
        yaxis=dict(gridcolor=GRID, tickfont=dict(color="#8b9ab5"),
                   title=None, zeroline=False),
    )
    st.plotly_chart(fig_trend, use_container_width=True)

with col_pie:
    st.markdown("""
    <div style='font-family:Syne,sans-serif;font-size:18px;font-weight:700;
         color:#f0f4ff;margin-bottom:4px;'>🥧 Category Distribution</div>
    <div style='font-family:DM Sans,sans-serif;font-size:13px;color:#8b9ab5;
         margin-bottom:12px;'>Sales share by category</div>
    """, unsafe_allow_html=True)

    fig_cat = px.pie(
        df, names="category", values="sales_amount",
        hole=0.54,
        color_discrete_sequence=["#a855f7","#ec4899","#f97316","#14f1d9","#ffd700"],
        template="plotly_dark"
    )
    fig_cat.update_traces(
        marker=dict(line=dict(color="#020617", width=3)),
        textfont=dict(family="Space Mono, monospace", color="#f0f4ff", size=12),
        hovertemplate="<b>%{label}</b><br>$%{value:,.0f} · %{percent}<extra></extra>"
    )
    fig_cat.update_layout(
        **CHART_CFG,
        height=380,
        legend=dict(
            font=dict(color="#f0f4ff", size=13),
            bgcolor="rgba(0,0,0,0)",
        )
    )
    st.plotly_chart(fig_cat, use_container_width=True)

# ============================================================
#  PRODUCT PERFORMANCE  +  QUANTITY BY REGION
# ============================================================
st.markdown("""
<div class="section-hdr">
    <div class="section-dot" style="background:#ff2d78;box-shadow:0 0 10px #ff2d78;"></div>
    <div class="section-hdr-text">Product & Quantity Breakdown</div>
    <div class="section-line"></div>
</div>
""", unsafe_allow_html=True)

col_prod, col_qty = st.columns(2, gap="large")

with col_prod:
    st.markdown("""
    <div style='font-family:Syne,sans-serif;font-size:18px;font-weight:700;
         color:#f0f4ff;margin-bottom:4px;'>🚀 Top Products</div>
    <div style='font-family:DM Sans,sans-serif;font-size:13px;color:#8b9ab5;
         margin-bottom:12px;'>Revenue ranked by product</div>
    """, unsafe_allow_html=True)

    product_df = (
        df.groupby("product")["sales_amount"].sum()
        .reset_index().sort_values("sales_amount", ascending=True)
    )
    fig_prod = px.bar(
        product_df, x="sales_amount", y="product", orientation="h",
        color="sales_amount",
        color_continuous_scale=[[0,"#1a0030"],[0.5,"#bf00ff"],[1,"#ff2d78"]],
        template="plotly_dark"
    )
    fig_prod.update_traces(
        marker_line_width=0,
        hovertemplate="<b>%{y}</b><br>$%{x:,.0f}<extra></extra>"
    )
    fig_prod.update_layout(
        **CHART_CFG,
        height=380,
        coloraxis_showscale=False,
        xaxis=dict(gridcolor=GRID, tickfont=dict(color="#8b9ab5"),
                   title=None, zeroline=False),
        yaxis=dict(showgrid=False, tickfont=dict(color="#f0f4ff", size=13),
                   title=None),
    )
    st.plotly_chart(fig_prod, use_container_width=True)

with col_qty:
    st.markdown("""
    <div style='font-family:Syne,sans-serif;font-size:18px;font-weight:700;
         color:#f0f4ff;margin-bottom:4px;'>📦 Quantity by Region</div>
    <div style='font-family:DM Sans,sans-serif;font-size:13px;color:#8b9ab5;
         margin-bottom:12px;'>Units sold per region</div>
    """, unsafe_allow_html=True)

    qty_df = (
        df.groupby("region")["quantity"].sum()
        .reset_index().sort_values("quantity", ascending=True)
    )
    fig_qty = px.bar(
        qty_df, x="quantity", y="region", orientation="h",
        color="quantity",
        color_continuous_scale=[[0,"#002020"],[0.5,"#00f5ff"],[1,"#00e5a0"]],
        template="plotly_dark"
    )
    fig_qty.update_traces(
        marker_line_width=0,
        hovertemplate="<b>%{y}</b><br>%{x:,} units<extra></extra>"
    )
    fig_qty.update_layout(
        **CHART_CFG,
        height=380,
        coloraxis_showscale=False,
        xaxis=dict(gridcolor=GRID, tickfont=dict(color="#8b9ab5"),
                   title=None, zeroline=False),
        yaxis=dict(showgrid=False, tickfont=dict(color="#f0f4ff", size=13),
                   title=None),
    )
    st.plotly_chart(fig_qty, use_container_width=True)

# ============================================================
#  FOOTER
# ============================================================
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div class="lab-footer">
    Advanced Analytics Lab · Powered by <span>Python</span> · <span>Streamlit</span> · <span>Plotly</span>
</div>
""", unsafe_allow_html=True)