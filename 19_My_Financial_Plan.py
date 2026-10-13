from datetime import date
import streamlit as st
from components.styling import page_header, disclosure
from services.financial_health import assess
from services.reporting import build_report
from utils.currency import format_inr

page_header("My Financial Plan", "Your data from every module in one place, with simple rule-based next steps.")
p = st.session_state.get("profile"); ind = assess(**p) if p else {}
tasks = st.session_state.get("tasks"); goals = st.session_state.get("household_goals"); pol = st.session_state.get("policies")
if not p: st.info("Complete the Financial Health Passport to unlock your snapshot.")
else:
    c = st.columns(3); c[0].metric("Monthly surplus", format_inr(ind["surplus"]["value"])); em = ind["emergency_months"]["value"]
    c[1].metric("Emergency cover", "Not provided" if em is None else f"{em:.1f} months"); c[2].metric("Net worth", format_inr(ind["net_worth"]["value"]))
actions, missing = [], []
if not p: actions.append("Complete the Financial Health Passport.")
else:
    if ind["surplus"]["value"] is not None and ind["surplus"]["value"] < 0: actions.append("Spending is above income: review expenses while keeping required EMIs paid.")
    if em is not None and em < 3: actions.append("Emergency cover is under 3 months of essentials: consider building it first.")
    if ind["dti"]["value"] and ind["dti"]["value"] > 0.4: actions.append("EMIs take over 40% of income (a common caution level, not a rule): review the Debt Planner.")
if pol is None or pol.empty: actions.append("Record your insurance details to see missing items."); missing.append("Insurance policies")
if goals is None or goals.empty: missing.append("Goals")
if tasks is not None and not tasks.empty and ((~tasks["done"]) & (tasks["due"].dt.date < date.today())).any(): actions.append("Clear overdue tasks in the Calendar.")
st.subheader("Suggested actions (untick to dismiss)")
kept = [a for i, a in enumerate(actions) if st.checkbox(a, True, key=f"act_{i}")]
if not actions: st.write("No suggestions from the rules we have. This does not mean everything is fine.")
if missing: st.warning("Missing information: " + ", ".join(missing))
pri = st.multiselect("Your top priorities (max 3)", ["Emergency fund", "Clear debt", "Home", "Children's education", "Retirement", "Insurance review", "Tax organisation", "Travel"], max_selections=3)
notes = st.text_area("Monthly review notes")
gl = [] if goals is None or goals.empty else [f"{r['goal']}: {format_inr(r['saved'])} of {format_inr(r['target'])}" for _, r in goals.dropna(subset=['goal']).iterrows()]
tl = [] if tasks is None or tasks.empty else [t for t, d in zip(tasks["task"], tasks["done"]) if not d]
st.download_button("Download report (Markdown)", build_report(p, ind, gl, tl, notes, pri), "my_financial_plan.md", "text/markdown")
st.caption("Rules are simple and transparent, based only on what you entered. They are not personalised advice.")
disclosure()
