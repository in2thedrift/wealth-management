import streamlit as st
from components.styling import page_header, disclosure, explain
from services.emergency_fund import plan
from utils.currency import format_inr

page_header("Emergency Fund Simulator", "How long could you cope if income stopped?")
a, b = st.columns(2)
ess = a.number_input("Essential monthly expenses incl. EMIs (INR)", min_value=0.0, value=40000.0, step=1000.0)
cur = b.number_input("Accessible emergency savings (INR)", min_value=0.0, value=100000.0, step=5000.0)
tm = a.selectbox("Target coverage (months)", [3, 6, 9, 12], index=1)
con = b.number_input("Monthly contribution (INR)", min_value=0.0, value=10000.0, step=1000.0)
r = plan(ess, cur, tm, con)
c = st.columns(4)
c[0].metric("Target", format_inr(r["target"]))
c[1].metric("Coverage now", "Not provided" if r["coverage"] is None else f"{r['coverage']:.1f} months")
c[2].metric("Shortfall", format_inr(r["shortfall"]))
c[3].metric("Months to target", "Set a contribution" if r["months_to_target"] is None else str(r["months_to_target"]))
st.caption("Count only savings you can access quickly. Equity funds or locked-in deposits may fall in value or take time to withdraw.")
explain("Target = essential expenses x months. Coverage = savings / essential expenses. Months to target = shortfall / contribution, rounded up. Assumes no interest and unchanged expenses.")
disclosure()
