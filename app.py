import streamlit as st

st.set_page_config(
    page_title="AI BI Platform",
    layout="wide",
    page_icon="⚡",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');
html, body, [class*="css"], .stApp { font-family: 'DM Sans', sans-serif !important; }
.stApp { background: #0b0c14 !important; }
[data-testid="stSidebar"] { background: #0f1020 !important; border-right: 1px solid rgba(255,255,255,0.06) !important; }
.block-container { padding-top: 2.5rem !important; max-width: 960px !important; }

/* Sidebar auto-generated page nav links */
[data-testid="stSidebarNav"] a span p,
[data-testid="stSidebarNavLink"] span p,
section[data-testid="stSidebar"] nav a span p,
section[data-testid="stSidebar"] ul li a span p {
    color: #94a3b8 !important;
    font-size: 13.5px !important;
    font-weight: 400 !important;
}
[data-testid="stSidebarNav"] a:hover span p,
section[data-testid="stSidebar"] nav a:hover span p {
    color: #e2e8f0 !important;
}
[data-testid="stSidebarNav"] a[aria-current="page"] span p,
section[data-testid="stSidebar"] nav a[aria-current="page"] span p {
    color: #c4b5fd !important;
    font-weight: 500 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:12px 0 20px;">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:20px;">
        <div style="width:34px;height:34px;background:linear-gradient(135deg,#7c3aed,#3b82f6);
          border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:16px;">⚡</div>
        <div>
          <div style="font-family:'Syne',sans-serif;font-weight:700;font-size:14px;color:#e2e8f0;">AI BI Platform</div>
          <div style="font-size:10px;color:#334155;letter-spacing:0.06em;text-transform:uppercase;">Executive Analytics</div>
        </div>
      </div>
      <div style="font-size:10px;letter-spacing:0.1em;text-transform:uppercase;color:#1e293b;font-weight:600;margin-bottom:10px;">Navigation</div>
      <div style="display:flex;align-items:center;gap:10px;padding:9px 12px;background:rgba(130,90,255,0.15);border-radius:8px;margin-bottom:4px;">
        <span style="font-size:14px;">🏠</span>
        <span style="font-size:13px;color:#c4b5fd;font-weight:500;">Executive Overview</span>
      </div>
      <hr style="border:none;border-top:1px solid rgba(255,255,255,0.05);margin:14px 0;">
      <div style="padding:14px;background:rgba(130,90,255,0.07);border:1px solid rgba(130,90,255,0.15);border-radius:10px;margin-top:8px;">
        <div style="font-size:11px;color:#7c3aed;font-weight:600;letter-spacing:0.06em;text-transform:uppercase;margin-bottom:6px;">✦ AI Insight</div>
        <div style="font-size:12px;color:#475569;line-height:1.6;">Navigate to any module using the sidebar links.</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── Hero ─────────────────────────────────────────────────────
st.markdown("""
<div style="padding:30px 0 0;">

  <div style="display:inline-flex;align-items:center;gap:8px;background:rgba(130,90,255,0.12);
    border:1px solid rgba(130,90,255,0.28);border-radius:100px;padding:5px 16px;
    font-size:11px;font-weight:500;letter-spacing:0.08em;text-transform:uppercase;
    color:#a78bfa;margin-bottom:28px;">
    ✦ Executive Intelligence Suite
  </div>

  <h1 style="font-family:'Syne',sans-serif;font-size:clamp(38px,5vw,64px);font-weight:800;
    line-height:1.08;letter-spacing:-0.02em;color:#f1f5f9;margin:0 0 22px 0;">
    Advanced
    <span style="background:linear-gradient(120deg,#a78bfa 20%,#60a5fa 80%);
      -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">
      Analytics</span><br>
    for Modern Business
  </h1>

  <p style="font-size:18px;font-weight:300;line-height:1.7;color:#64748b;max-width:540px;margin:0 0 40px 0;">
    AI-powered business intelligence, SQL copilots, and executive insights —
    unified in one premium platform built for decision makers.
  </p>

  <div style="display:flex;gap:24px;margin-bottom:52px;">
    <div style="display:flex;align-items:center;gap:8px;font-size:13px;color:#475569;">
      <div style="width:7px;height:7px;border-radius:50%;background:#22c55e;box-shadow:0 0 6px #22c55e88;"></div>
      All systems operational
    </div>
    <div style="display:flex;align-items:center;gap:8px;font-size:13px;color:#475569;">
      <div style="width:7px;height:7px;border-radius:50%;background:#a78bfa;box-shadow:0 0 6px #a78bfa88;"></div>
      AI models active
    </div>
    <div style="display:flex;align-items:center;gap:8px;font-size:13px;color:#475569;">
      <div style="width:7px;height:7px;border-radius:50%;background:#60a5fa;box-shadow:0 0 6px #60a5fa88;"></div>
      Real-time data sync
    </div>
  </div>

</div>
""", unsafe_allow_html=True)

# ── Feature cards ────────────────────────────────────────────
col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.markdown("""
    <div style="background:#12131f;border:1px solid rgba(255,255,255,0.07);border-radius:16px;padding:26px 24px 24px;height:100%;">
      <div style="width:44px;height:44px;border-radius:12px;background:rgba(130,90,255,0.12);
        display:flex;align-items:center;justify-content:center;font-size:20px;margin-bottom:18px;">📊</div>
      <div style="font-family:'Syne',sans-serif;font-size:17px;font-weight:700;color:#e2e8f0;margin-bottom:10px;">Analytics Lab</div>
      <div style="font-size:14px;line-height:1.65;color:#475569;margin-bottom:20px;">
        Advanced business intelligence dashboards, KPI tracking, and performance analysis across all dimensions.
      </div>
      <span style="display:inline-block;font-size:11px;font-weight:500;letter-spacing:0.05em;padding:4px 11px;
        border-radius:6px;text-transform:uppercase;background:rgba(130,90,255,0.1);color:#a78bfa;">Dashboards</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background:#12131f;border:1px solid rgba(255,255,255,0.07);border-radius:16px;padding:26px 24px 24px;height:100%;">
      <div style="width:44px;height:44px;border-radius:12px;background:rgba(96,165,250,0.1);
        display:flex;align-items:center;justify-content:center;font-size:20px;margin-bottom:18px;">🧠</div>
      <div style="font-family:'Syne',sans-serif;font-size:17px;font-weight:700;color:#e2e8f0;margin-bottom:10px;">AI SQL Copilot</div>
      <div style="font-size:14px;line-height:1.65;color:#475569;margin-bottom:20px;">
        Ask complex business questions in plain language. Our AI translates intent into precise SQL queries instantly.
      </div>
      <span style="display:inline-block;font-size:11px;font-weight:500;letter-spacing:0.05em;padding:4px 11px;
        border-radius:6px;text-transform:uppercase;background:rgba(96,165,250,0.1);color:#60a5fa;">Natural Language</span>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background:#12131f;border:1px solid rgba(255,255,255,0.07);border-radius:16px;padding:26px 24px 24px;height:100%;">
      <div style="width:44px;height:44px;border-radius:12px;background:rgba(20,184,166,0.1);
        display:flex;align-items:center;justify-content:center;font-size:20px;margin-bottom:18px;">🗂️</div>
      <div style="font-family:'Syne',sans-serif;font-size:17px;font-weight:700;color:#e2e8f0;margin-bottom:10px;">Data Explorer</div>
      <div style="font-size:14px;line-height:1.65;color:#475569;margin-bottom:20px;">
        Deep-dive into datasets, schema structures, data completeness scores, and actionable quality insights.
      </div>
      <span style="display:inline-block;font-size:11px;font-weight:500;letter-spacing:0.05em;padding:4px 11px;
        border-radius:6px;text-transform:uppercase;background:rgba(20,184,166,0.1);color:#2dd4bf;">Exploration</span>
    </div>
    """, unsafe_allow_html=True)

# ── Footer ───────────────────────────────────────────────────
st.markdown("""
<div style="height:1px;background:linear-gradient(90deg,transparent,rgba(130,90,255,0.25) 40%,rgba(96,165,250,0.2) 60%,transparent);margin:48px 0 36px;"></div>
<div style="display:flex;align-items:center;gap:10px;background:rgba(255,255,255,0.03);
  border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:13px 18px;
  font-size:13px;color:#475569;width:fit-content;">
  ← Use the <span style="color:#a78bfa;font-weight:500;">&nbsp;sidebar&nbsp;</span> to navigate between platform modules
</div>
""", unsafe_allow_html=True)