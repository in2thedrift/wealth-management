import streamlit as st
from components.styling import page_header, disclosure
from utils.currency import format_inr
from utils.state import get_table

page_header("Family Finance Mode", "A single-user household workspace. Other family members cannot log in yet.")
st.info("Real multi-person access needs authentication, consent and per-person record isolation. This version does not pretend to have them: one person enters the household's information.")
g = get_table("household_goals", {"goal": "object", "target": "float64", "saved": "float64", "owner_label": "object"})
st.subheader("Shared goals")
g = st.data_editor(g, num_rows="dynamic", width="stretch", key="hg_ed"); st.session_state["household_goals"] = g
for _, r in g.dropna(subset=["goal"]).iterrows():
    if r["target"] and r["target"] > 0: st.progress(min(r["saved"] / r["target"], 1.0), text=f"{r['goal']}: {format_inr(r['saved'])} of {format_inr(r['target'])}")
st.subheader("Household obligations")
o = get_table("obligations", {"obligation": "object", "monthly_amount": "float64"}); o = st.data_editor(o, num_rows="dynamic", width="stretch", key="ob_ed"); st.session_state["obligations"] = o
st.metric("Monthly obligations", format_inr(float(o["monthly_amount"].sum())))
st.subheader("Shared document checklist")
for i, d in enumerate(["Where important documents are kept", "Who knows the nominee details", "Insurance policy list shared", "Emergency contacts"]): st.checkbox(d, key=f"fd_{i}")
disclosure()
