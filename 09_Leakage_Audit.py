import streamlit as st
from components.styling import page_header, disclosure
from services import transaction_analysis as ta
from utils.currency import format_inr

page_header("Financial Leakage Audit", "Patterns worth a second look. These are suspicions, not confirmed problems.")
tx = st.session_state.get("txns")
if tx is None or tx.empty:
    st.info("Add or import transactions in the Budget and Expense Manager first."); st.stop()
rec, dup, big, small = ta.recurring(tx), ta.possible_duplicates(tx), ta.unusually_large(tx), ta.repeated_small(tx)
st.subheader("Suspected recurring payments")
if rec.empty: st.write("None found.")
else:
    rec = rec.copy(); rec["review"] = False
    ed = st.data_editor(rec.round(0), width="stretch", disabled=["description", "months_seen", "monthly_amount", "annual_cost"], key="leak_ed")
    f = ed[ed["review"]]
    st.metric("Flagged for review", f"{format_inr(f['monthly_amount'].sum())} / month", f"{format_inr(f['annual_cost'].sum())} / year if cancelled", delta_color="off")
    st.caption("Nothing is cancelled for you. Cancel only what you confirm you no longer need.")
for title, d in [("Possible duplicate charges (same date, description, amount)", dup), ("Unusually large expenses", big), ("Repeated small expenses (5+ in a month)", small)]:
    st.subheader(title); st.dataframe(d, width="stretch") if len(d) else st.write("None found.")
disclosure()
