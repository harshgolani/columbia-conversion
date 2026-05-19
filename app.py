import json
import pandas as pd
import streamlit as st # type: ignore
from src.charts import (
    chart_conversion_donut, chart_model_comparison,
    chart_pagevalues_effect, chart_monthly_conversion,
    chart_exit_rate, chart_browsing_depth
)

st.set_page_config(
    page_title="Columbia Turkey — Conversion Analysis",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
#MainMenu, header[data-testid="stHeader"], footer,
[data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"], [data-testid="stSidebar"] { display: none; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background-color: #0a0a0a; color: #e8e0dc;
}
.block-container { padding: 0 2.5rem 2rem; max-width: 1200px; margin: auto; }

.kpi-sticky { position: sticky; top: 0; z-index: 999; background: #0a0a0a; padding: 0.85rem 0 0.6rem; }
.kpi-row { display: flex; gap: 12px; }
.kpi-card { flex: 1; background: #111; border-radius: 8px; padding: 0.9rem 1.25rem 0.8rem; border: 1px solid #1e1614; }
.kpi-number { color: #c4a090; font-size: 1.75rem; font-weight: 600; font-family: Inter, system-ui, sans-serif; line-height: 1.1; letter-spacing: -0.5px; }
.kpi-label { color: #5a4e4a; font-size: 0.68rem; font-family: 'Courier New', monospace; letter-spacing: 0.14em; text-transform: uppercase; margin-top: 0.3rem; }

[data-testid="stTabs"] { margin-top: 0.1rem; }
[data-testid="stTabBar"] { background: transparent; border-bottom: 1px solid #1e1614; }
button[data-baseweb="tab"] { background: transparent !important; color: #7a6a65 !important; font-family: 'Courier New', monospace !important; font-size: 0.70rem !important; letter-spacing: 0.15em !important; text-transform: uppercase !important; padding: 0.65rem 1.25rem !important; border-bottom: 2px solid transparent !important; }
button[data-baseweb="tab"][aria-selected="true"] { color: #c4a090 !important; border-bottom: 2px solid #c4a090 !important; }
button[data-baseweb="tab"]:hover { color: #c4a090 !important; }
[data-baseweb="tab-highlight"], [data-baseweb="tab-border"] { display: none; }

.insight-panel { background: #111; border: 1px solid #1e1614; border-radius: 8px; padding: 0.9rem 1.25rem; margin-top: 0.6rem; display: flex; flex-direction: column; gap: 0; }
.insight-row { display: flex; align-items: baseline; gap: 1rem; padding: 0.55rem 0; }
.insight-row + .insight-row { border-top: 1px solid #1a1210; }
.insight-label { color: #c4a090; font-family: 'Courier New', monospace; font-size: 0.60rem; letter-spacing: 0.18em; text-transform: uppercase; white-space: nowrap; min-width: 9.5rem; }
.insight-text { color: #c4b8b4; font-size: 0.875rem; font-family: Inter, system-ui, sans-serif; line-height: 1.5; }

.rec-table { width: 100%; border-collapse: collapse; margin-top: 0.5rem; font-family: Inter, system-ui, sans-serif; font-size: 0.875rem; }
.rec-table th { background: #c4a090; color: #0a0a0a; font-weight: 600; padding: 0.75rem 1rem; text-align: left; font-size: 0.75rem; letter-spacing: 0.08em; text-transform: uppercase; }
.rec-table td { padding: 0.75rem 1rem; color: #c4b8b4; vertical-align: top; line-height: 1.5; border-bottom: 1px solid #1a1210; }
.rec-table tr:nth-child(even) td { background: #0f0d0c; }
.rec-table tr:nth-child(odd) td { background: #111; }
.rec-table td:first-child { color: #c4a090; font-weight: 600; white-space: nowrap; }

.model-callout { background: #111; border: 1px solid #1e1614; border-radius: 8px; padding: 0.9rem 1.25rem; margin-top: 1.2rem; display: flex; align-items: center; gap: 1rem; }
.model-callout-text { color: #c4b8b4; font-size: 0.875rem; font-family: Inter, system-ui, sans-serif; line-height: 1.5; font-style: italic; }
</style>
""", unsafe_allow_html=True)


def load_precomputed():
    with open('assets/precomputed.json', 'r') as f:
        data = json.load(f)
    return (
        data['overview'],
        pd.DataFrame(data['models']),
        pd.DataFrame(data['pv_effect']),
        data['pv_dist'],
        pd.DataFrame(data['monthly']),
        pd.DataFrame(data['exit_rate']),
        pd.DataFrame(data['browsing']),
        pd.DataFrame(data['recommendations'])
    )

overview, models, pv_effect, pv_dist, monthly, exit_df, browsing_df, recs = load_precomputed()


def insight_panel(finding, why, recommendation):
    return f"""
<div class="insight-panel">
  <div class="insight-row">
    <span class="insight-label">Finding</span>
    <span class="insight-text">{finding}</span>
  </div>
  <div class="insight-row">
    <span class="insight-label">Why It Matters</span>
    <span class="insight-text">{why}</span>
  </div>
  <div class="insight-row">
    <span class="insight-label">Recommendation</span>
    <span class="insight-text">{recommendation}</span>
  </div>
</div>"""


# ── KPI bar ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="kpi-sticky">
  <div class="kpi-row">
    <div class="kpi-card"><div class="kpi-number">12,330</div><div class="kpi-label">Total Sessions</div></div>
    <div class="kpi-card"><div class="kpi-number">15.5%</div><div class="kpi-label">Conversion Rate</div></div>
    <div class="kpi-card"><div class="kpi-number">5–6%</div><div class="kpi-label">Industry Average</div></div>
    <div class="kpi-card"><div class="kpi-number">+6.4%</div><div class="kpi-label">Revenue from 1% Lift</div></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "The Problem", "Model Results", "PageValues Effect",
    "Behavioral Patterns", "Recommendations"
])

# ── Tab 1: The Problem ────────────────────────────────────────────────────────
with tab1:
    st.plotly_chart(chart_conversion_donut(overview), use_container_width=True)
    st.markdown(insight_panel(
        finding="84.5% of 12,330 sessions end without a purchase — the opportunity is in recovering non-converters, not optimizing the 15.5% who already buy.",
        why="Columbia Turkey converts at <strong>15.5%</strong> vs a <strong>5–6% industry average</strong> — this is brand-driven traffic. The barrier is friction, not awareness.",
        recommendation="A 1% conversion improvement adds <strong>123 purchases</strong> — a <strong>6.4% revenue increase</strong> without acquiring a single additional visitor.",
    ), unsafe_allow_html=True)

# ── Tab 2: Model Results ──────────────────────────────────────────────────────
with tab2:
    st.plotly_chart(chart_model_comparison(models), use_container_width=True)
    st.markdown(insight_panel(
        finding="Keras Neural Network achieves AUC <strong>0.9306</strong> on cross-validation and <strong>0.9377</strong> on holdout — the narrow gap confirms no overfitting.",
        why="PPV of 0.61 means <strong>39% of predicted converters won't actually buy</strong> — precision limitations matter when targeting promotions at scale.",
        recommendation="Use the model to <strong>flag high-risk sessions for intervention</strong>, not as a binary trigger for promotions — precision cost is too high.",
    ), unsafe_allow_html=True)

# ── Tab 3: PageValues Effect ──────────────────────────────────────────────────
with tab3:
    st.plotly_chart(chart_pagevalues_effect(pv_effect), use_container_width=True)
    st.markdown(insight_panel(
        finding="Conversion spikes from <strong>8% to 55%+</strong> the moment PageValues rises above zero — yet <strong>77.9% of sessions</strong> never reach a high-value page.",
        why="PageValues accounts for <strong>100% relative importance</strong> in SHAP analysis — it dominates all other features combined. The funnel breaks before checkout.",
        recommendation="Surface high-value pages earlier via personalized recommendations, Best Sellers modules, and smarter internal search ranking.",
    ), unsafe_allow_html=True)

# ── Tab 4: Behavioral Patterns ────────────────────────────────────────────────
with tab4:
    col_left, col_right = st.columns(2)
    with col_left:
        st.plotly_chart(chart_monthly_conversion(monthly), use_container_width=True)
    with col_right:
        st.plotly_chart(chart_exit_rate(exit_df), use_container_width=True)

    st.plotly_chart(chart_browsing_depth(browsing_df), use_container_width=True)

    st.markdown(insight_panel(
        finding="November converts at <strong>25.4%</strong> — 2.3x the baseline. Exit rate increases drop conversion <strong>30%</strong>. Users browsing 80+ product pages convert <strong>25% less</strong> than focused shoppers.",
        why="The November spike is driven by <strong>winter onset in Turkey</strong> (Istanbul avg 10–17°C), not Black Friday — a durable, predictable seasonal signal. High browsing depth signals <strong>comparison shopping across competitor sites</strong>, not engagement.",
        recommendation="Invest in lower-intent months with loyalty programs. Deploy exit-intent popups. Add internal comparison tools to reduce cross-site browsing.",
    ), unsafe_allow_html=True)

# ── Tab 5: Recommendations ────────────────────────────────────────────────────
with tab5:
    rows = ""
    for _, row in recs.iterrows():
        rows += f"""
    <tr>
        <td>{row['feature']}</td>
        <td>{row['finding']}</td>
        <td>{row['action']}</td>
        <td>{row['tradeoff']}</td>
    </tr>"""

    st.markdown(f"""
<table class="rec-table">
  <thead><tr><th>Feature</th><th>Finding</th><th>Action</th><th>Tradeoff</th></tr></thead>
  <tbody>{rows}</tbody>
</table>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="model-callout">
  <span class="model-callout-text">The model doesn't convert the customer. It tells you exactly where to intervene.</span>
</div>
""", unsafe_allow_html=True)
