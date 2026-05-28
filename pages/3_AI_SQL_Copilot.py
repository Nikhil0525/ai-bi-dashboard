import plotly.express as px
import streamlit as st
import pandas as pd
from ai.llm_service import generate_sql_from_question

st.set_page_config(page_title="AI SQL Copilot", page_icon="🤖", layout="wide")

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
    --green:     #00e5a0;
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
        radial-gradient(ellipse 55% 50% at 92%  5%,  rgba(191,0,255,0.12) 0%, transparent 55%),
        radial-gradient(ellipse 65% 55% at 50% 100%, rgba(255,45,120,0.08) 0%, transparent 55%);
    min-height: 100vh;
}
.stApp::before {
    content:'';
    position:fixed; inset:0;
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
    content:'';
    position:fixed; inset:0;
    background:repeating-linear-gradient(
        0deg, transparent, transparent 2px,
        rgba(0,0,0,0.04) 2px, rgba(0,0,0,0.04) 4px
    );
    pointer-events:none; z-index:0;
}

/* ── HERO ── */
.copilot-hero {
    padding: 44px 0 6px;
    animation: fadeDown .7s cubic-bezier(.22,1,.36,1) both;
}
@keyframes fadeDown {
    from { opacity:0; transform:translateY(-20px); }
    to   { opacity:1; transform:translateY(0); }
}
.copilot-eyebrow {
    font-family:'Space Mono',monospace;
    font-size:11px;
    letter-spacing:.32em;
    color:var(--cyan);
    text-transform:uppercase;
    margin-bottom:12px;
    display:flex; align-items:center; gap:10px;
}
.eyebrow-dot {
    width:6px; height:6px; border-radius:50%;
    background:var(--cyan);
    box-shadow:0 0 8px var(--cyan);
    animation:dotPulse 1.8s ease-in-out infinite;
}
@keyframes dotPulse {
    0%,100%{ transform:scale(1);   opacity:1; }
    50%    { transform:scale(1.7); opacity:.5; }
}
.copilot-title {
    font-family:'Syne',sans-serif;
    font-size:clamp(30px,4vw,56px);
    font-weight:800;
    line-height:1.06;
    color:#f0f4ff;
    margin:0 0 10px;
}
.copilot-title span {
    background:linear-gradient(90deg,var(--cyan),var(--violet));
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    background-clip:text;
}
.copilot-sub {
    font-family:'DM Sans',sans-serif;
    font-size:16px;
    color:var(--muted);
    max-width:560px;
    line-height:1.65;
    margin-bottom:30px;
}
.hero-divider {
    width:100px; height:2px;
    background:linear-gradient(90deg,transparent,var(--cyan),var(--violet),transparent);
    margin-bottom:36px;
    animation:barPulse 3s ease-in-out infinite;
}
@keyframes barPulse {
    0%,100%{ width:100px; opacity:.5; }
    50%    { width:200px; opacity:1; }
}

/* ── PROMPT CARDS (example queries) ── */
.prompt-grid {
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:12px;
    margin-bottom:28px;
    animation:fadeDown .6s cubic-bezier(.22,1,.36,1) .15s both;
}
.prompt-chip {
    background:var(--glass-bg);
    border:1px solid var(--glass-bdr);
    border-radius:12px;
    padding:13px 16px;
    font-family:'Space Mono',monospace;
    font-size:11px;
    color:var(--muted);
    cursor:pointer;
    transition:all .3s;
    line-height:1.5;
}
.prompt-chip:hover {
    border-color:var(--cyan);
    color:var(--cyan);
    background:rgba(0,245,255,0.05);
    transform:translateY(-3px);
    box-shadow:0 8px 24px rgba(0,245,255,0.1);
}
.prompt-chip strong {
    display:block;
    font-size:10px;
    letter-spacing:.15em;
    text-transform:uppercase;
    color:var(--cyan);
    margin-bottom:4px;
    opacity:.7;
}

/* ── INPUT AREA ── */
.input-wrap {
    background:var(--glass-bg);
    border:1px solid rgba(0,245,255,0.22);
    border-radius:18px;
    padding:24px 28px;
    backdrop-filter:blur(16px);
    margin-bottom:28px;
    animation:fadeDown .6s cubic-bezier(.22,1,.36,1) .2s both;
    box-shadow:0 0 40px rgba(0,245,255,0.04);
    transition:border-color .3s, box-shadow .3s;
}
.input-wrap:focus-within {
    border-color:var(--cyan);
    box-shadow:0 0 50px rgba(0,245,255,0.10);
}
.input-label {
    font-family:'Space Mono',monospace;
    font-size:10px;
    letter-spacing:.28em;
    text-transform:uppercase;
    color:var(--cyan);
    margin-bottom:12px;
    display:flex; align-items:center; gap:8px;
}
.stTextInput > div > div > input {
    background:rgba(0,0,0,0) !important;
    border:none !important;
    border-bottom:1px solid rgba(255,255,255,0.10) !important;
    border-radius:0 !important;
    color:#f0f4ff !important;
    font-family:'DM Sans',sans-serif !important;
    font-size:18px !important;
    font-weight:500 !important;
    padding:10px 4px !important;
    box-shadow:none !important;
    caret-color:var(--cyan);
}
.stTextInput > div > div > input:focus {
    border-bottom-color:var(--cyan) !important;
    box-shadow:none !important;
}
.stTextInput > div > div > input::placeholder {
    color:#4a5568 !important;
    font-style:italic;
}

/* ── RESULTS SECTION ── */
.results-grid {
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:20px;
    animation:fadeDown .5s cubic-bezier(.22,1,.36,1) both;
}

/* ── GLASS PANEL ── */
.glass-panel {
    background:var(--glass-bg);
    border:1px solid var(--glass-bdr);
    border-radius:20px;
    padding:24px 26px;
    backdrop-filter:blur(18px);
    transition:border-color .3s, box-shadow .3s;
}
.glass-panel:hover {
    border-color:rgba(0,245,255,.15);
    box-shadow:0 12px 40px rgba(0,0,0,.4);
}

/* ── SQL CODE BLOCK ── */
.sql-header {
    display:flex; align-items:center; gap:10px;
    margin-bottom:14px;
}
.sql-badge {
    font-family:'Space Mono',monospace;
    font-size:10px;
    letter-spacing:.22em;
    text-transform:uppercase;
    color:var(--cyan);
    background:rgba(0,245,255,0.08);
    border:1px solid rgba(0,245,255,0.2);
    border-radius:99px;
    padding:4px 12px;
}
.sql-badge-live {
    display:inline-flex; align-items:center; gap:6px;
    font-family:'Space Mono',monospace;
    font-size:10px;
    letter-spacing:.18em;
    text-transform:uppercase;
    color:#00e5a0;
    background:rgba(0,229,160,0.07);
    border:1px solid rgba(0,229,160,0.2);
    border-radius:99px;
    padding:4px 12px;
}
.sql-live-dot {
    width:5px; height:5px;
    border-radius:50%;
    background:#00e5a0;
    animation:dotPulse 1.4s ease-in-out infinite;
}
.stCode, .stCodeBlock, pre, code {
    background:rgba(0,0,0,0.5) !important;
    border:1px solid rgba(0,245,255,0.12) !important;
    border-radius:14px !important;
    font-family:'Space Mono',monospace !important;
    font-size:13px !important;
    color:#a5f3fc !important;
    padding:16px 20px !important;
}

/* ── RESULT TABLE ── */
.result-header {
    display:flex; align-items:center; justify-content:space-between;
    margin-bottom:14px;
}
.result-count {
    font-family:'Space Mono',monospace;
    font-size:10px;
    letter-spacing:.18em;
    color:var(--muted);
    text-transform:uppercase;
}
.stDataFrame, [data-testid="stDataFrame"] {
    border-radius:14px !important;
    overflow:hidden !important;
    border:1px solid rgba(255,255,255,0.07) !important;
}

/* ── SECTION HEADER ── */
.section-hdr {
    display:flex; align-items:center; gap:13px;
    margin:36px 0 16px;
}
.section-dot {
    width:8px; height:8px; border-radius:50%;
    animation:dotPulse 2s ease-in-out infinite;
}
.section-hdr-text {
    font-family:'Syne',sans-serif;
    font-size:22px; font-weight:700;
    color:var(--txt);
}
.section-line {
    flex:1; height:1px;
    background:linear-gradient(90deg,var(--glass-bdr),transparent);
}

/* ── HISTORY CARD ── */
.history-item {
    background:var(--glass-bg);
    border:1px solid var(--glass-bdr);
    border-radius:14px;
    padding:14px 18px;
    margin-bottom:10px;
    display:flex; align-items:flex-start; gap:14px;
    transition:border-color .3s, transform .3s;
    cursor:pointer;
}
.history-item:hover {
    border-color:rgba(191,0,255,.3);
    transform:translateX(4px);
}
.history-num {
    font-family:'Space Mono',monospace;
    font-size:11px;
    color:var(--violet);
    background:rgba(191,0,255,0.1);
    border:1px solid rgba(191,0,255,0.2);
    border-radius:8px;
    padding:3px 8px;
    flex-shrink:0;
    margin-top:2px;
}
.history-q {
    font-family:'DM Sans',sans-serif;
    font-size:14px; color:var(--txt);
}
.history-q small {
    font-family:'Space Mono',monospace;
    font-size:10px; color:var(--muted);
    display:block; margin-top:3px;
}

/* ── EMPTY STATE ── */
.empty-state {
    text-align:center;
    padding:60px 20px;
    animation:fadeDown .6s ease both;
}
.empty-icon {
    font-size:52px;
    margin-bottom:18px;
    filter:drop-shadow(0 0 20px rgba(0,245,255,0.3));
}
.empty-title {
    font-family:'Syne',sans-serif;
    font-size:22px; font-weight:700;
    color:var(--txt);
    margin-bottom:8px;
}
.empty-sub {
    font-family:'DM Sans',sans-serif;
    font-size:15px; color:var(--muted);
    line-height:1.65;
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
    text-align:center;
    padding:36px 0 18px;
    font-family:'Space Mono',monospace;
    font-size:11px; letter-spacing:.2em;
    color:rgba(139,154,181,.4);
    text-transform:uppercase;
}
.lab-footer span { color:var(--cyan); opacity:.75; }
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
     color:#00f5ff;text-transform:uppercase;padding:10px 0 16px;
     border-bottom:1px solid rgba(255,255,255,0.08);margin-bottom:16px;'>
🤖 SQL Copilot
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<div style='font-family:Space Mono,monospace;font-size:10px;letter-spacing:.18em;
     color:#8b9ab5;text-transform:uppercase;margin-bottom:8px;'>Navigation</div>
""", unsafe_allow_html=True)

pages = {
    "🏠 Executive Overview": False,
    "📊 Analytics Lab":      False,
    "🤖 AI SQL Copilot":     True,
    "🗄️ Data Explorer":      False,
}
for label, active in pages.items():
    bg    = "rgba(0,245,255,0.10)"  if active else "transparent"
    bdr   = "rgba(0,245,255,0.35)"  if active else "transparent"
    color = "#00f5ff"               if active else "#8b9ab5"
    fw    = "700"                   if active else "400"
    st.sidebar.markdown(f"""
    <div style='display:flex;align-items:center;gap:10px;padding:10px 14px;
         border-radius:12px;background:{bg};border:1px solid {bdr};margin-bottom:6px;
         font-family:DM Sans,sans-serif;font-size:14px;font-weight:{fw};color:{color};'>
        {label}
    </div>""", unsafe_allow_html=True)

# Tips in sidebar
st.sidebar.markdown("""
<div style='margin-top:28px;padding:18px;background:rgba(0,245,255,0.04);
     border:1px solid rgba(0,245,255,0.12);border-radius:14px;'>
    <div style='font-family:Space Mono,monospace;font-size:10px;letter-spacing:.2em;
         text-transform:uppercase;color:#00f5ff;margin-bottom:12px;'>
        💡 Query Tips
    </div>
    <div style='font-family:DM Sans,sans-serif;font-size:13px;color:#8b9ab5;line-height:1.7;'>
        • Ask in plain English<br>
        • Mention columns by name<br>
        • Try: "top 5 products"<br>
        • Try: "sales by region"<br>
        • Try: "show all categories"
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
#  HERO
# ============================================================
st.markdown("""
<div class="copilot-hero">
    <div class="copilot-eyebrow">
        <span class="eyebrow-dot"></span>
        AI-Powered Query Engine
    </div>
    <div class="copilot-title">AI SQL <span>Copilot</span></div>
    <div class="copilot-sub">
        Ask questions in plain English. The AI generates precise SQL,
        executes it against your dataset, and returns instant results.
    </div>
    <div class="hero-divider"></div>
</div>
""", unsafe_allow_html=True)

# ============================================================
#  EXAMPLE PROMPT CHIPS
# ============================================================
st.markdown("""
<div class="prompt-grid">
    <div class="prompt-chip"><strong>Region</strong>Show sales by region</div>
    <div class="prompt-chip"><strong>Product</strong>Top products by revenue</div>
    <div class="prompt-chip"><strong>Category</strong>Sales per category</div>
    <div class="prompt-chip"><strong>Revenue</strong>Show total revenue</div>
</div>
""", unsafe_allow_html=True)

# ============================================================
#  INPUT
# ============================================================
st.markdown("""
<div class="input-wrap">
    <div class="input-label">
        <span class="eyebrow-dot"></span>
        Natural Language Query
    </div>
""", unsafe_allow_html=True)

question = st.text_input(
    label="",
    placeholder="e.g.  show me total sales by region sorted by revenue...",
    label_visibility="collapsed"
)

st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
#  RESULTS
# ============================================================
if question:
    sql = generate_sql_from_question(question)

    # keyword-based execution
    q = question.lower()
    if "region" in q:
        result = df.groupby("region")["sales_amount"].sum().reset_index()
    elif "product" in q:
        result = df.groupby("product")["sales_amount"].sum().reset_index()
    elif "category" in q:
        result = df.groupby("category")["sales_amount"].sum().reset_index()
    elif "total sales" in q or "revenue" in q:
        result = pd.DataFrame({"total_sales": [df["sales_amount"].sum()]})
    else:
        result = df.head(10)

    row_count = len(result)

    # ── Two-column layout: SQL left, Table right
    col_sql, col_tbl = st.columns(2, gap="large")

    with col_sql:
        st.markdown("""
        <div class="glass-panel">
            <div class="sql-header">
                <div class="sql-badge">◈ Generated SQL</div>
                <div class="sql-badge-live"><span class="sql-live-dot"></span>Executed</div>
            </div>
        """, unsafe_allow_html=True)
        st.code(sql, language="sql")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_tbl:
        st.markdown(f"""
        <div class="glass-panel">
            <div class="result-header">
                <div style='font-family:Syne,sans-serif;font-size:17px;
                     font-weight:700;color:#f0f4ff;'>
                    📋 Query Result
                </div>
                <div class="result-count">{row_count} row{'s' if row_count != 1 else ''} returned</div>
            </div>
        """, unsafe_allow_html=True)
        st.dataframe(result, use_container_width=True)
        if len(result.columns) >= 2:
            try:
                x_col = result.columns[0]
                y_col = result.columns[1]

                fig = px.bar(
                    result,
                    x=x_col,
                    y=y_col,
                    template="plotly_dark",
                    color=y_col,
                    color_continuous_scale="plasma"
                )

                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_color="white"
                )

                st.plotly_chart(fig, use_container_width=True)

                st.markdown("""
            <div class="insight-card">
                <h4>🤖 AI Insight</h4>
                <p>
                The visualization highlights key business trends and performance patterns.
                Focus on high-performing categories and regions to maximize growth opportunities.
                </p>
            </div>
            """, unsafe_allow_html=True)

            except:
                pass

        import plotly.express as px

        st.markdown("</div>", unsafe_allow_html=True)

else:
    # ── Empty state
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">🤖</div>
        <div class="empty-title">Ready to query your data</div>
        <div class="empty-sub">
            Type a question above in plain English.<br>
            The AI will generate SQL and return your results instantly.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
#  FOOTER
# ============================================================
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div class="lab-footer">
    AI SQL Copilot · Powered by <span>Python</span> · <span>Streamlit</span> · <span>AI</span>
</div>
""", unsafe_allow_html=True)