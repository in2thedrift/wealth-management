import streamlit as st
import plotly.graph_objects as go
from components.styling import page_header, disclosure
from config import BRAND_NAME, TAGLINE
from data.sample_data import DEMO_PROFILE
from services.financial_health import assess
from utils.currency import format_inr

page_header(f"Welcome to {BRAND_NAME}", TAGLINE)
demo = st.toggle("Demo mode (fictional sample data)", value=False)
p = DEMO_PROFILE if demo else st.session_state.get("profile")
if demo:
    st.info("Demo mode: all numbers below are fictional and do not belong to you.")
if not p:
    st.info("No data yet. Fill in the Financial Health Passport, or switch on demo mode to preview the dashboard.")
    st.stop()
r = assess(**p)
c = st.columns(4)
c[0].metric("Monthly surplus", format_inr(r["surplus"]["value"]))
sr = r["savings_rate"]["value"]
c[1].metric("Savings rate", "Not provided" if sr is None else f"{sr:.0%}")
em = r["emergency_months"]["value"]
c[2].metric("Emergency cover", "Not provided" if em is None else f"{em:.1f} months")
c[3].metric("Net worth (estimate)", format_inr(r["net_worth"]["value"]))
left, right = st.columns(2)
fig = go.Figure(go.Bar(x=["Income", "Spending + EMIs"], y=[p["income"], p["essential"] + p["discretionary"] + p["emi_total"]],
                       marker_color=["#0F8B8D", "#12284C"]))
fig.update_layout(title="Income vs expenses (monthly)", height=320, margin=dict(t=50, b=20))
left.plotly_chart(fig, width="stretch")
fig2 = go.Figure(go.Pie(labels=["Essential", "Discretionary", "EMIs"], values=[p["essential"], p["discretionary"], p["emi_total"]], hole=0.55))
fig2.update_layout(title="Spending breakdown", height=320, margin=dict(t=50, b=20))
right.plotly_chart(fig2, width="stretch")
t = st.session_state.get("tasks")
st.subheader("Upcoming tasks")
if t is None or t.empty: st.write("No tasks yet. Add reminders in the Personal Finance Calendar.")
else: st.dataframe(t[~t["done"]].sort_values("due")[["task", "category", "due"]].head(5), width="stretch")
disclosure()
