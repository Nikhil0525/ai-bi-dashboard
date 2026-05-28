import streamlit as st
import pandas as pd

st.set_page_config(page_title="Data Explorer", page_icon="🗄️", layout="wide")

# ============================================================
#  PREMIUM CSS
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --cyan:      #00f5ff;
    --violet:    #bf00ff;
    --pink:      #ff2d78;
    --gold:      #ffd700;
    --green:     #00e5a0;
    --orange:    #ff7b2c;
    --glass-bg:  rgba(255,255,255,0.04);
    --glass-bdr: rgba(255,255,255,0.10);
    --txt:       #f0f4ff;
    --muted:     #8b9ab5;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--txt);
}

/* ── BACKGROUND ── */
.stApp {
    background: #020617;
    background-image:
        radial-gradient(ellipse 80% 55% at 8%   0%,  rgba(0,245,255,0.10) 0%, transparent 58%),
        radial-gradient(ellipse 55% 50% at 92%  5%,  rgba(255,215,0,0.08)  0%, transparent 55%),
        radial-gradient(ellipse 65% 55% at 50% 100%, rgba(0,229,160,0.07)  0%, transparent 55%);
    min-height: 100vh;
}
.stApp::before {
    content:''; position:fixed; inset:0;
    background-image:
        linear-gradient(rgba(0,245,255,0.028) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,245,255,0.028) 1px, transparent 1px);
    background-size:60px 60px;
    animation:gridScroll 22s linear infinite;
    pointer-events:none; z-index:0;
}
@keyframes gridScroll {
    0%  { background-position:0 0; }
    100%{ background-position:60px 60px; }
}
.stApp::after {
    content:''; position:fixed; inset:0;
    background:repeating-linear-gradient(
        0deg, transparent, transparent 2px,
        rgba(0,0,0,0.04) 2px, rgba(0,0,0,0.04) 4px
    );
    pointer-events:none; z-index:0;
}

/* ── HERO ── */
.explorer-hero {
    padding:44px 0 6px;
    animation:fadeDown .7s cubic-bezier(.22,1,.36,1) both;
}
@keyframes fadeDown {
    from { opacity:0; transform:translateY(-20px); }
    to   { opacity:1; transform:translateY(0); }
}
.explorer-eyebrow {
    font-family:'Space Mono',monospace;
    font-size:11px; letter-spacing:.32em;
    color:var(--gold); text-transform:uppercase;
    margin-bottom:12px;
    display:flex; align-items:center; gap:10px;
}
.eyebrow-dot {
    width:6px; height:6px; border-radius:50%;
    background:var(--gold); box-shadow:0 0 8px var(--gold);
    animation:dotPulse 1.8s ease-in-out infinite;
}
@keyframes dotPulse {
    0%,100%{ transform:scale(1);   opacity:1; }
    50%    { transform:scale(1.7); opacity:.5; }
}
.explorer-title {
    font-family:'Syne',sans-serif;
    font-size:clamp(30px,4vw,56px); font-weight:800;
    line-height:1.06; color:#f0f4ff; margin:0 0 10px;
}
.explorer-title span {
    background:linear-gradient(90deg,var(--gold),var(--orange));
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    background-clip:text;
}
.explorer-sub {
    font-family:'DM Sans',sans-serif;
    font-size:16px; color:var(--muted);
    max-width:520px; line-height:1.65; margin-bottom:30px;
}
.hero-divider {
    width:100px; height:2px;
    background:linear-gradient(90deg,transparent,var(--gold),var(--orange),transparent);
    margin-bottom:36px;
    animation:barPulse 3s ease-in-out infinite;
}
@keyframes barPulse {
    0%,100%{ width:100px; opacity:.5; }
    50%    { width:200px; opacity:1; }
}

/* ── STATS CARDS ── */
.stats-row {
    display:grid;
    grid-template-columns:repeat(5,1fr);
    gap:14px;
    margin-bottom:28px;
}
.stat-card {
    position:relative;
    background:var(--glass-bg);
    border:1px solid var(--glass-bdr);
    border-radius:18px;
    padding:22px 20px;
    backdrop-filter:blur(16px);
    overflow:hidden;
    transition:transform .35s cubic-bezier(.22,1,.36,1), box-shadow .35s;
    animation:cardUp .6s cubic-bezier(.22,1,.36,1) both;
}
.stat-card:nth-child(1){ animation-delay:.08s; --sa:var(--cyan);   }
.stat-card:nth-child(2){ animation-delay:.14s; --sa:var(--green);  }
.stat-card:nth-child(3){ animation-delay:.20s; --sa:var(--violet); }
.stat-card:nth-child(4){ animation-delay:.26s; --sa:var(--gold);   }
.stat-card:nth-child(5){ animation-delay:.32s; --sa:var(--pink);   }
@keyframes cardUp {
    from { opacity:0; transform:translateY(26px) scale(.97); }
    to   { opacity:1; transform:translateY(0)    scale(1); }
}
.stat-card::before {
    content:''; position:absolute;
    top:0; left:0; right:0; height:2px;
    background:linear-gradient(90deg,transparent,var(--sa),transparent);
}
.stat-card::after {
    content:''; position:absolute;
    bottom:-50px; right:-50px;
    width:110px; height:110px; border-radius:50%;
    background:radial-gradient(circle,var(--sa) 0%,transparent 70%);
    opacity:.07; transition:opacity .3s;
}
.stat-card:hover {
    transform:translateY(-7px) scale(1.02);
    box-shadow:0 18px 50px rgba(0,0,0,.5), 0 0 26px var(--sa);
    border-color:var(--sa);
}
.stat-card:hover::after { opacity:.16; }
.stat-icon { font-size:20px; margin-bottom:10px; display:block; }
.stat-label {
    font-family:'Space Mono',monospace;
    font-size:9px; letter-spacing:.22em;
    text-transform:uppercase; color:var(--muted); margin-bottom:5px;
}
.stat-value {
    font-family:'Syne',sans-serif;
    font-size:26px; font-weight:800;
    color:var(--sa);
    text-shadow:0 0 18px var(--sa);
    line-height:1.1;
}
.stat-sub {
    font-family:'DM Sans',sans-serif;
    font-size:11px; color:var(--muted); margin-top:5px;
}

/* ── SECTION HEADER ── */
.section-hdr {
    display:flex; align-items:center; gap:13px;
    margin:32px 0 14px;
}
.section-dot {
    width:8px; height:8px; border-radius:50%;
    animation:dotPulse 2s ease-in-out infinite;
}
.section-hdr-text {
    font-family:'Syne',sans-serif;
    font-size:21px; font-weight:700; color:var(--txt);
}
.section-line {
    flex:1; height:1px;
    background:linear-gradient(90deg,var(--glass-bdr),transparent);
}

/* ── FILTER BAR ── */
.filter-bar {
    background:var(--glass-bg);
    border:1px solid var(--glass-bdr);
    border-radius:16px;
    padding:18px 22px;
    backdrop-filter:blur(16px);
    display:flex; align-items:center; gap:16px;
    margin-bottom:18px;
    flex-wrap:wrap;
}
.filter-label {
    font-family:'Space Mono',monospace;
    font-size:10px; letter-spacing:.22em;
    text-transform:uppercase; color:var(--muted);
    white-space:nowrap;
}

/* ── STREAMLIT WIDGETS ── */
.stSelectbox > div > div,
.stTextInput > div > div > input,
.stMultiSelect > div > div {
    background:rgba(0,0,0,0.3) !important;
    border:1px solid rgba(255,215,0,0.18) !important;
    border-radius:10px !important;
    color:var(--txt) !important;
    font-family:'DM Sans',sans-serif !important;
    font-size:14px !important;
}
.stSelectbox > div > div:focus-within,
.stTextInput > div > div > input:focus {
    border-color:var(--gold) !important;
    box-shadow:0 0 0 3px rgba(255,215,0,0.10) !important;
}
.stTextInput > div > div > input::placeholder { color:#4a5568 !important; }

/* ── DATA TABLE ── */
.stDataFrame, [data-testid="stDataFrame"] {
    border-radius:16px !important;
    overflow:hidden !important;
    border:1px solid rgba(255,215,0,0.10) !important;
    box-shadow:0 4px 24px rgba(0,0,0,0.35) !important;
}

/* ── GLASS PANEL ── */
.glass-panel {
    background:var(--glass-bg);
    border:1px solid var(--glass-bdr);
    border-radius:20px;
    padding:22px 26px;
    backdrop-filter:blur(18px);
    transition:border-color .3s, box-shadow .3s;
}
.glass-panel:hover {
    border-color:rgba(255,215,0,0.18);
    box-shadow:0 10px 36px rgba(0,0,0,.4);
}

/* ── DTYPE BADGE ── */
.dtype-row {
    display:flex; align-items:center;
    justify-content:space-between;
    padding:11px 0;
    border-bottom:1px solid rgba(255,255,255,0.05);
    font-family:'DM Sans',sans-serif;
    font-size:14px; color:var(--txt);
    transition:background .2s;
}
.dtype-row:last-child { border-bottom:none; }
.dtype-row:hover { background:rgba(255,255,255,0.025); border-radius:8px; padding:11px 8px; }
.dtype-col { font-family:'Space Mono',monospace; font-size:13px; color:#e2e8f0; }
.dtype-badge {
    font-family:'Space Mono',monospace;
    font-size:10px; letter-spacing:.12em;
    padding:3px 12px; border-radius:99px;
    text-transform:uppercase;
}
.dtype-int    { background:rgba(0,245,255,0.10);  border:1px solid rgba(0,245,255,0.22);  color:var(--cyan);   }
.dtype-float  { background:rgba(0,229,160,0.10);  border:1px solid rgba(0,229,160,0.22);  color:var(--green);  }
.dtype-object { background:rgba(168,85,247,0.10); border:1px solid rgba(168,85,247,0.22); color:#a855f7;       }
.dtype-date   { background:rgba(255,215,0,0.10);  border:1px solid rgba(255,215,0,0.22);  color:var(--gold);   }
.dtype-bool   { background:rgba(255,45,120,0.10); border:1px solid rgba(255,45,120,0.22); color:var(--pink);   }
.dtype-other  { background:rgba(255,123,44,0.10); border:1px solid rgba(255,123,44,0.22); color:var(--orange); }

/* ── NULL HEATMAP BARS ── */
.null-row {
    display:flex; align-items:center; gap:14px;
    padding:9px 0;
    border-bottom:1px solid rgba(255,255,255,0.04);
}
.null-row:last-child { border-bottom:none; }
.null-col-name {
    font-family:'Space Mono',monospace;
    font-size:12px; color:#e2e8f0;
    width:150px; flex-shrink:0;
}
.null-bar-wrap {
    flex:1; height:8px; border-radius:99px;
    background:rgba(255,255,255,0.05);
    overflow:hidden;
}
.null-bar-fill {
    height:100%; border-radius:99px;
    background:linear-gradient(90deg,var(--green),var(--cyan));
    transition:width .6s cubic-bezier(.22,1,.36,1);
}
.null-bar-fill.has-nulls {
    background:linear-gradient(90deg,var(--pink),var(--violet));
}
.null-pct {
    font-family:'Space Mono',monospace;
    font-size:11px; color:var(--muted);
    width:48px; text-align:right; flex-shrink:0;
}

/* ── DOWNLOAD ── */
.stDownloadButton > button {
    background:linear-gradient(135deg,rgba(255,215,0,0.10),rgba(255,123,44,0.08)) !important;
    border:1px solid rgba(255,215,0,0.28) !important;
    color:var(--gold) !important;
    border-radius:12px !important;
    font-family:'Space Mono',monospace !important;
    font-size:12px !important; letter-spacing:.1em !important;
    padding:12px 28px !important;
    transition:all .3s !important;
}
.stDownloadButton > button:hover {
    background:linear-gradient(135deg,rgba(255,215,0,0.20),rgba(255,123,44,0.14)) !important;
    box-shadow:0 0 24px rgba(255,215,0,0.20) !important;
    transform:translateY(-2px) !important;
}

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
.lab-footer {
    text-align:center; padding:36px 0 18px;
    font-family:'Space Mono',monospace;
    font-size:11px; letter-spacing:.2em;
    color:rgba(139,154,181,.4); text-transform:uppercase;
}
.lab-footer span { color:var(--gold); opacity:.8; }
</style>
""", unsafe_allow_html=True)

# ============================================================
#  DATA
# ============================================================
df = pd.read_csv("data/dataset.csv")

# ============================================================
#  SIDEBAR
# ============================================================
st.sidebar.markdown("""
<div style='font-family:Space Mono,monospace;font-size:13px;letter-spacing:.15em;
     color:#ffd700;text-transform:uppercase;padding:10px 0 16px;
     border-bottom:1px solid rgba(255,255,255,0.08);margin-bottom:16px;'>
🗄️ Data Explorer
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<div style='font-family:Space Mono,monospace;font-size:10px;letter-spacing:.18em;
     color:#8b9ab5;text-transform:uppercase;margin-bottom:8px;'>Navigation</div>
""", unsafe_allow_html=True)

pages = {
    "🏠 Executive Overview": False,
    "📊 Analytics Lab":      False,
    "🤖 AI SQL Copilot":     False,
    "🗄️ Data Explorer":      True,
}
for label, active in pages.items():
    bg    = "rgba(255,215,0,0.10)"  if active else "transparent"
    bdr   = "rgba(255,215,0,0.35)"  if active else "transparent"
    color = "#ffd700"               if active else "#8b9ab5"
    fw    = "700"                   if active else "400"
    st.sidebar.markdown(f"""
    <div style='display:flex;align-items:center;gap:10px;padding:10px 14px;
         border-radius:12px;background:{bg};border:1px solid {bdr};margin-bottom:6px;
         font-family:DM Sans,sans-serif;font-size:14px;font-weight:{fw};color:{color};'>
        {label}
    </div>""", unsafe_allow_html=True)

# Sidebar column filter
st.sidebar.markdown("""
<div style='margin-top:24px;font-family:Space Mono,monospace;font-size:10px;
     letter-spacing:.18em;text-transform:uppercase;color:#8b9ab5;margin-bottom:8px;'>
🔍 Filter Columns
</div>""", unsafe_allow_html=True)

all_cols       = df.columns.tolist()
visible_cols   = st.sidebar.multiselect("", all_cols, default=all_cols,
                                         label_visibility="collapsed")
if not visible_cols:
    visible_cols = all_cols

# ============================================================
#  HERO
# ============================================================
st.markdown("""
<div class="explorer-hero">
    <div class="explorer-eyebrow">
        <span class="eyebrow-dot"></span>
        Dataset Intelligence Suite
    </div>
    <div class="explorer-title">Data <span>Explorer</span></div>
    <div class="explorer-sub">
        Inspect, filter, and understand every dimension of your dataset —
        schema, nulls, types, and raw records at a glance.
    </div>
    <div class="hero-divider"></div>
</div>
""", unsafe_allow_html=True)

# ============================================================
#  STATS CARDS
# ============================================================
rows      = df.shape[0]
cols      = df.shape[1]
nulls     = int(df.isnull().sum().sum())
num_cols  = len(df.select_dtypes(include="number").columns)
cat_cols  = len(df.select_dtypes(include="object").columns)

st.markdown(f"""
<div class="stats-row">
  <div class="stat-card">
    <span class="stat-icon">📋</span>
    <div class="stat-label">Total Rows</div>
    <div class="stat-value">{rows:,}</div>
    <div class="stat-sub">Records in dataset</div>
  </div>
  <div class="stat-card">
    <span class="stat-icon">🧩</span>
    <div class="stat-label">Columns</div>
    <div class="stat-value">{cols}</div>
    <div class="stat-sub">Fields per record</div>
  </div>
  <div class="stat-card">
    <span class="stat-icon">🔮</span>
    <div class="stat-label">Missing Values</div>
    <div class="stat-value">{nulls}</div>
    <div class="stat-sub">{'Clean dataset ✓' if nulls == 0 else 'Nulls detected'}</div>
  </div>
  <div class="stat-card">
    <span class="stat-icon">🔢</span>
    <div class="stat-label">Numeric Cols</div>
    <div class="stat-value">{num_cols}</div>
    <div class="stat-sub">Quantitative fields</div>
  </div>
  <div class="stat-card">
    <span class="stat-icon">🏷️</span>
    <div class="stat-label">Categorical</div>
    <div class="stat-value">{cat_cols}</div>
    <div class="stat-sub">Text / label fields</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
#  SEARCH + TABLE
# ============================================================
st.markdown("""
<div class="section-hdr">
    <div class="section-dot" style="background:var(--gold);box-shadow:0 0 10px var(--gold);"></div>
    <div class="section-hdr-text">📂 Raw Dataset</div>
    <div class="section-line"></div>
</div>
""", unsafe_allow_html=True)

search_col, dl_col = st.columns([5, 1], gap="small")

with search_col:
    search_term = st.text_input("", placeholder="🔍  Search across all columns...",
                                 label_visibility="collapsed")

filtered_df = df[visible_cols].copy()

if search_term:
    mask = filtered_df.apply(
        lambda col: col.astype(str).str.contains(search_term, case=False, na=False)
    ).any(axis=1)
    filtered_df = filtered_df[mask]

st.markdown(f"""
<div style='font-family:Space Mono,monospace;font-size:10px;letter-spacing:.18em;
     text-transform:uppercase;color:var(--muted);margin:-4px 0 12px;'>
    Showing {len(filtered_df):,} of {rows:,} records · {len(visible_cols)} columns visible
</div>
""", unsafe_allow_html=True)

st.dataframe(filtered_df, use_container_width=True, height=420)

with dl_col:
    st.markdown("<div style='padding-top:4px'></div>", unsafe_allow_html=True)
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="⬇️ Export CSV",
        data=csv,
        file_name="dataset_export.csv",
        mime="text/csv"
    )

# ============================================================
#  SCHEMA  +  NULL HEATMAP  (side by side)
# ============================================================
import streamlit.components.v1 as components

st.markdown("""
<div class="section-hdr">
    <div class="section-dot" style="background:#bf00ff;box-shadow:0 0 10px #bf00ff;"></div>
    <div class="section-hdr-text">Schema & Quality</div>
    <div class="section-line"></div>
</div>
""", unsafe_allow_html=True)

col_schema, col_null = st.columns(2, gap="large")

# ── dtype helper
def dtype_badge(dt):
    s = str(dt)
    if "int"      in s: return "integer",  "#00f5ff",  "rgba(0,245,255,0.10)",  "rgba(0,245,255,0.22)"
    if "float"    in s: return "float",    "#00e5a0",  "rgba(0,229,160,0.10)",  "rgba(0,229,160,0.22)"
    if "object"   in s: return "string",   "#a855f7",  "rgba(168,85,247,0.10)", "rgba(168,85,247,0.22)"
    if "datetime" in s: return "datetime", "#ffd700",  "rgba(255,215,0,0.10)",  "rgba(255,215,0,0.22)"
    if "bool"     in s: return "boolean",  "#ff2d78",  "rgba(255,45,120,0.10)", "rgba(255,45,120,0.22)"
    return s,            "#ff7b2c",  "rgba(255,123,44,0.10)", "rgba(255,123,44,0.22)"

# ── Schema / dtypes — rendered via components.html (no sanitization)
with col_schema:
    rows_html = ""
    for col_name, dtype in df.dtypes.items():
        label, color, bg, border = dtype_badge(dtype)
        null_count = int(df[col_name].isnull().sum())
        null_html  = (
            f"<span style='color:#ff2d78;font-size:10px;font-family:Space Mono,monospace;"
            f"background:rgba(255,45,120,0.08);border:1px solid rgba(255,45,120,0.2);"
            f"border-radius:99px;padding:2px 8px;'>⚠ {null_count} null</span>"
        ) if null_count else ""
        rows_html += f"""
        <div style='display:flex;align-items:center;justify-content:space-between;
             padding:11px 14px;border-bottom:1px solid rgba(255,255,255,0.05);
             transition:background .2s;border-radius:6px;'>
            <span style='font-family:Space Mono,monospace;font-size:13px;color:#e2e8f0;'>
                {col_name}
            </span>
            <div style='display:flex;align-items:center;gap:8px;'>
                {null_html}
                <span style='font-family:Space Mono,monospace;font-size:10px;
                      letter-spacing:.12em;text-transform:uppercase;padding:3px 12px;
                      border-radius:99px;background:{bg};border:1px solid {border};
                      color:{color};'>
                    {label}
                </span>
            </div>
        </div>"""

    panel_schema = f"""
    <div style='background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.10);
         border-radius:20px;padding:8px 0;backdrop-filter:blur(18px);'>
        <div style='font-family:Syne,sans-serif;font-size:17px;font-weight:700;
             color:#f0f4ff;padding:14px 18px 10px;'>🧬 Column Schema</div>
        {rows_html}
    </div>"""

    panel_h = 80 + len(df.columns) * 47
    components.html(panel_schema, height=panel_h, scrolling=False)

# ── Null completeness heatmap
with col_null:
    null_rows_html = ""
    total_rows = len(df)
    for col_name in df.columns:
        null_count   = int(df[col_name].isnull().sum())
        complete_pct = ((total_rows - null_count) / total_rows) * 100
        bar_grad     = (
            "linear-gradient(90deg,#ff2d78,#bf00ff)" if null_count > 0
            else "linear-gradient(90deg,#00e5a0,#00f5ff)"
        )
        null_rows_html += f"""
        <div style='display:flex;align-items:center;gap:14px;padding:11px 14px;
             border-bottom:1px solid rgba(255,255,255,0.04);border-radius:6px;'>
            <div style='font-family:Space Mono,monospace;font-size:12px;color:#e2e8f0;
                 width:130px;flex-shrink:0;overflow:hidden;text-overflow:ellipsis;
                 white-space:nowrap;'>{col_name}</div>
            <div style='flex:1;height:8px;border-radius:99px;
                 background:rgba(255,255,255,0.06);overflow:hidden;'>
                <div style='width:{complete_pct:.1f}%;height:100%;border-radius:99px;
                     background:{bar_grad};'></div>
            </div>
            <div style='font-family:Space Mono,monospace;font-size:11px;color:#8b9ab5;
                 width:42px;text-align:right;flex-shrink:0;'>{complete_pct:.0f}%</div>
        </div>"""

    panel_null = f"""
    <div style='background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.10);
         border-radius:20px;padding:8px 0;backdrop-filter:blur(18px);'>
        <div style='font-family:Syne,sans-serif;font-size:17px;font-weight:700;
             color:#f0f4ff;padding:14px 18px 10px;'>🧪 Data Completeness</div>
        {null_rows_html}
    </div>"""

    components.html(panel_null, height=panel_h, scrolling=False)

# ============================================================
#  SUMMARY STATS
# ============================================================
st.markdown("""
<div class="section-hdr" style="margin-top:36px;">
    <div class="section-dot" style="background:var(--cyan);box-shadow:0 0 10px var(--cyan);"></div>
    <div class="section-hdr-text">📊 Summary Statistics</div>
    <div class="section-line"></div>
</div>
""", unsafe_allow_html=True)

numeric_df = df.select_dtypes(include="number")
if not numeric_df.empty:
    st.dataframe(
        numeric_df.describe().round(2),
        use_container_width=True
    )
else:
    st.markdown("""
    <div style='font-family:DM Sans,sans-serif;font-size:14px;color:var(--muted);
         padding:20px 0;'>No numeric columns found in dataset.</div>
    """, unsafe_allow_html=True)

# ============================================================
#  FOOTER
# ============================================================
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div class="lab-footer">
    Data Explorer · Powered by <span>Python</span> · <span>Streamlit</span> · <span>Pandas</span>
</div>
""", unsafe_allow_html=True)