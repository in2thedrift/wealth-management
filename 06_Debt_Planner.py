import pandas as pd, streamlit as st
from components.styling import page_header, disclosure, explain
from services.debt import simulate_payoff
from services.calculators import emi, amortization_schedule
from utils.currency import format_inr

page_header("Debt and EMI Planner", "Compare repayment strategies. Always keep paying required EMIs.")
df = st.data_editor(pd.DataFrame([
    {"name": "Home loan", "balance": 2500000.0, "rate": 8.5, "emi": 25000.0},
    {"name": "Credit card", "balance": 80000.0, "rate": 36.0, "emi": 5000.0}]), num_rows="dynamic", width="stretch")
extra = st.number_input("Extra monthly payment (INR)", min_value=0.0, value=5000.0, step=1000.0)
debts = df.dropna().to_dict("records")
if debts:
    cols = st.columns(3)
    base = simulate_payoff(debts, 0)
    for col, strat in zip(cols[:2], ["avalanche", "snowball"]):
        r = simulate_payoff(debts, extra, strat)
        col.metric(f"{strat.title()} + extra", f"{r['months']} months", f"Interest {format_inr(r['interest'])}", delta_color="off")
    cols[2].metric("Current plan (no extra)", f"{base['months']} months", f"Interest {format_inr(base['interest'])}", delta_color="off")
    if not base["cleared"]:
        st.warning("At least one EMI does not cover its interest, so the debt is not cleared within 100 years. Check the entries.")
with st.expander("EMI calculator and schedule"):
    p = st.number_input("Principal", min_value=0.0, value=1000000.0, step=10000.0)
    rt = st.number_input("Annual rate (%)", min_value=0.0, value=9.0)
    n = st.number_input("Tenure (months)", min_value=1, value=120)
    st.metric("EMI", format_inr(emi(p, rt, int(n))))
    st.dataframe(pd.DataFrame(amortization_schedule(p, rt, int(n))).round(2), width="stretch")
explain("Interest accrues monthly at rate/12. Payments are made at month end. Rates are assumed fixed; prepayment charges are not modelled. Avalanche = highest rate first; snowball = smallest balance first. Freed-up EMIs roll into the remaining debts.")
disclosure()
