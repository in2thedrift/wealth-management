import streamlit as st
from components.styling import page_header, disclosure
from services.financial_health import assess
from utils.currency import format_inr

page_header("Financial Health Passport", "A transparent snapshot. Every indicator shows its formula and limits.")
with st.form("health"):
    a, b = st.columns(2)
    income = a.number_input("Monthly take-home income (INR)", min_value=0.0, step=1000.0)
    essential = b.number_input("Essential monthly expenses (INR)", min_value=0.0, step=1000.0)
    disc = a.number_input("Discretionary expenses (INR)", min_value=0.0, step=500.0)
    emis = b.number_input("Monthly EMIs and debt payments (INR)", min_value=0.0, step=500.0)
    liquid = a.number_input("Liquid savings (INR)", min_value=0.0, step=5000.0)
    assets = b.number_input("Total assets, optional (INR)", min_value=0.0, step=10000.0)
    liabs = a.number_input("Total liabilities, optional (INR)", min_value=0.0, step=10000.0)
    go = st.form_submit_button("Save and calculate", type="primary")
if go:
    st.session_state["profile"] = dict(income=income, essential=essential, discretionary=disc, emi_total=emis,
        liquid_savings=liquid, assets=assets or None, liabilities=liabs or None)
    st.success("Saved for this session only. Closing the tab clears it.")
p = st.session_state.get("profile")
if not p:
    st.info("Enter your numbers above to see your indicators.")
    st.stop()
for k, ind in assess(**p).items():
    v = ind["value"]
    shown = "Not provided" if v is None else (format_inr(v) if k in ("surplus", "net_worth") else
            (f"{v:.1f} months" if k == "emergency_months" else f"{v:.1%}"))
    with st.container(border=True):
        st.subheader(f"{ind['label']}: {shown}")
        st.markdown(f"**Formula:** {ind['formula']}  \n**Meaning:** {ind['meaning']}  \n**Does not tell you:** {ind['limits']}")
disclosure()
