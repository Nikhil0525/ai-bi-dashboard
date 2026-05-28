import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(page_title="Forecasting", page_icon="📈", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');
html, body, [class*="css"], .stApp { font-family: 'DM Sans', sans-serif !important; }
.stApp { background: #0b0c14 !important; }
.block-container { padding-top: 2rem !important; max-width: 1100px !important; }
[data-testid="stSidebarNav"] { display: none !important; }
[data-testid="stSidebar"] { background: #0f1020 !important; border-right: 1px solid rgba(255,255,255,0.06) !important; }
div[data-testid="stSelectbox"] label { color: #64748b !important; font-size: 13px !important; }
[data-testid="stSidebar"] a[data-testid="stPageLink"] { border-radius: 8px !important; margin-bottom: 2px !important; }
[data-testid="stSidebar"] a[data-testid="stPageLink"]:hover { background: rgba(255,255,255,0.04) !important; }
[data-testid="stSidebar"] a[data-testid="stPageLink"] p { color: #64748b !important; font-size: 13px !important; }
[data-testid="stSidebar"] a[data-testid="stPageLink"]:hover p { color: #e2e8f0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:12px 0 16px;">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:20px;">
        <div style="width:34px;height:34px;background:linear-gradient(135deg,#7c3aed,#3b82f6);
          border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:16px;">⚡</div>
        <div>
          <div style="font-family:'Syne',sans-serif;font-weight:700;font-size:14px;color:#e2e8f0;">AI BI Platform</div>
          <div style="font-size:10px;color:#334155;letter-spacing:0.06em;text-transform:uppercase;">Executive Analytics</div>
        </div>
      </div>
      <div style="font-size:10px;letter-spacing:0.1em;text-transform:uppercase;color:#334155;font-weight:600;margin-bottom:8px;">Navigation</div>
    </div>
    """, unsafe_allow_html=True)

    # Inactive pages as real clickable links
    st.page_link("pages/1_Executive_Overview.py", label="🏠  Executive Overview")
    st.page_link("pages/2_Analytics_Lab.py",      label="📊  Analytics Lab")
    st.page_link("pages/3_AI_SQL_Copilot.py",     label="🧠  AI SQL Copilot")
    st.page_link("pages/4_Data_Explorer.py",      label="🗂️  Data Explorer")

    # Active page — highlighted pill
    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;padding:9px 12px;
      background:rgba(130,90,255,0.18);border:1px solid rgba(130,90,255,0.28);
      border-radius:8px;margin-top:2px;">
      <span>📈</span>
      <span style="font-size:13px;color:#c4b5fd;font-weight:600;">Forecasting</span>
    </div>
    <hr style="border:none;border-top:1px solid rgba(255,255,255,0.05);margin:14px 0;">
    <div style="padding:14px;background:rgba(96,165,250,0.07);border:1px solid rgba(96,165,250,0.15);border-radius:10px;">
      <div style="font-size:11px;color:#60a5fa;font-weight:600;letter-spacing:0.06em;text-transform:uppercase;margin-bottom:6px;">📈 Forecasting</div>
      <div style="font-size:12px;color:#94a3b8;line-height:1.6;">Sales trend analysis. Add your prediction model below.</div>
    </div>
    """, unsafe_allow_html=True)

# ── Load data ────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("data/dataset.csv")
    df["order_date"] = pd.to_datetime(df["order_date"])
    return df

df = load_data()

# ── Page header ──────────────────────────────────────────────
st.markdown("""
<div style="padding: 10px 0 32px;">
  <div style="display:inline-flex;align-items:center;gap:8px;background:rgba(96,165,250,0.1);
    border:1px solid rgba(96,165,250,0.25);border-radius:100px;padding:5px 16px;
    font-size:11px;font-weight:500;letter-spacing:0.08em;text-transform:uppercase;
    color:#60a5fa;margin-bottom:20px;">📈 Forecasting Module</div>
  <h1 style="font-family:'Syne',sans-serif;font-size:clamp(28px,4vw,46px);font-weight:800;
    line-height:1.1;letter-spacing:-0.02em;color:#f1f5f9;margin:0 0 10px 0;">
    Sales <span style="background:linear-gradient(120deg,#60a5fa 20%,#a78bfa 80%);
      -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">Forecasting</span>
  </h1>
  <p style="font-size:15px;font-weight:300;color:#475569;margin:0;">
    Historical sales trends and forward-looking performance analysis.
  </p>
</div>
""", unsafe_allow_html=True)

# ── KPIs ─────────────────────────────────────────────────────
trend = df.groupby("order_date")["sales_amount"].sum().reset_index().sort_values("order_date")
total = df["sales_amount"].sum()
latest_day = trend.iloc[-1]["sales_amount"] if len(trend) else 0
avg_daily = trend["sales_amount"].mean()
num_days = trend["order_date"].nunique()

def kpi_card(label, value, sub, color):
    return f"""<div style="background:#12131f;border:1px solid rgba(255,255,255,0.07);
      border-radius:14px;padding:20px 22px;">
      <div style="font-size:11px;color:#475569;letter-spacing:0.05em;text-transform:uppercase;font-weight:500;margin-bottom:8px;">{label}</div>
      <div style="font-size:26px;font-family:'Syne',sans-serif;font-weight:700;color:{color};margin-bottom:4px;">{value}</div>
      <div style="font-size:12px;color:#64748b;">{sub}</div>
    </div>"""

c1, c2, c3, c4 = st.columns(4, gap="medium")
with c1: st.markdown(kpi_card("Total Revenue", f"${total:,.0f}", "all time", "#a78bfa"), unsafe_allow_html=True)
with c2: st.markdown(kpi_card("Latest Day", f"${latest_day:,.0f}", trend.iloc[-1]["order_date"].strftime("%b %d") if len(trend) else "—", "#60a5fa"), unsafe_allow_html=True)
with c3: st.markdown(kpi_card("Avg Daily Sales", f"${avg_daily:,.0f}", "per day", "#2dd4bf"), unsafe_allow_html=True)
with c4: st.markdown(kpi_card("Days Tracked", f"{num_days}", "data points", "#f59e0b"), unsafe_allow_html=True)

st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

# ── Controls ─────────────────────────────────────────────────
ca, cb = st.columns([2, 1], gap="medium")
with ca: granularity = st.selectbox("Granularity", ["Daily", "Weekly", "Monthly"], index=2)
with cb: show_markers = st.selectbox("Markers", ["Show", "Hide"], index=0)

# ── Aggregate ────────────────────────────────────────────────
if granularity == "Weekly":
    trend_agg = df.groupby(df["order_date"].dt.to_period("W").apply(lambda r: r.start_time))["sales_amount"].sum().reset_index()
elif granularity == "Monthly":
    trend_agg = df.groupby(df["order_date"].dt.to_period("M").apply(lambda r: r.start_time))["sales_amount"].sum().reset_index()
else:
    trend_agg = trend.copy()
trend_agg.columns = ["order_date", "sales_amount"]
trend_agg = trend_agg.sort_values("order_date")

# ── Chart ────────────────────────────────────────────────────
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=trend_agg["order_date"], y=trend_agg["sales_amount"],
    mode="lines+markers" if show_markers == "Show" else "lines",
    line=dict(color="#7c3aed", width=2.5),
    marker=dict(size=6, color="#a78bfa", line=dict(color="#0b0c14", width=1.5)),
    fill="tozeroy", fillcolor="rgba(124,58,237,0.08)",
    hovertemplate="<b>%{x|%b %d, %Y}</b><br>Sales: $%{y:,.0f}<extra></extra>"
))
fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#0f1020",
    font=dict(family="DM Sans", color="#64748b", size=12),
    title=dict(text=f"{granularity} Sales Trend", font=dict(family="Syne", size=18, color="#e2e8f0"), x=0, xanchor="left", pad=dict(l=4, b=16)),
    xaxis=dict(gridcolor="rgba(255,255,255,0.04)", linecolor="rgba(255,255,255,0.06)", tickcolor="rgba(0,0,0,0)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.04)", linecolor="rgba(255,255,255,0.06)", tickprefix="$", tickformat=",.0f"),
    hovermode="x unified", hoverlabel=dict(bgcolor="#1e1b2e", font_color="#e2e8f0", bordercolor="#7c3aed"),
    margin=dict(l=0, r=0, t=52, b=0), height=420,
)
st.plotly_chart(fig, use_container_width=True)

# ── Prediction placeholder ────────────────────────────────────
st.markdown("""
<div style="background:#12131f;border:1px solid rgba(96,165,250,0.2);border-radius:14px;padding:28px;margin-top:8px;">
  <div style="display:flex;align-items:center;gap:12px;margin-bottom:10px;">
    <div style="width:36px;height:36px;border-radius:10px;background:rgba(96,165,250,0.1);
      display:flex;align-items:center;justify-content:center;font-size:18px;">🔮</div>
    <div style="font-family:'Syne',sans-serif;font-size:16px;font-weight:700;color:#e2e8f0;">Prediction Engine</div>
    <span style="font-size:11px;font-weight:500;padding:3px 10px;border-radius:6px;
      text-transform:uppercase;background:rgba(245,158,11,0.1);color:#f59e0b;margin-left:4px;">Coming Soon</span>
  </div>
  <p style="font-size:14px;color:#475569;line-height:1.65;margin:0;">
    Drop in your Prophet, ARIMA, or sklearn model here. The chart above will extend with a forecast band.
  </p>
</div>
""", unsafe_allow_html=True)