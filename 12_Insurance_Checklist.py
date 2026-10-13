import streamlit as st
from components.styling import page_header, disclosure
from utils.state import get_table

page_header("Insurance and Protection Checklist", "Organise your policies and learn what to ask. No product recommendations.")
df = get_table("policies", {"type": "object", "insurer": "object", "sum_assured": "float64", "annual_premium": "float64", "renewal_date": "datetime64[ns]", "nominee_recorded": "bool"})
df = st.data_editor(df, num_rows="dynamic", width="stretch", key="pol_ed", column_config={
    "type": st.column_config.SelectboxColumn(options=["Health", "Term life", "Personal accident", "Disability", "Employer cover", "Other"]),
    "renewal_date": st.column_config.DateColumn(), "nominee_recorded": st.column_config.CheckboxColumn("Nominee recorded")})
st.session_state["policies"] = df
if df.empty: st.info("Add a policy above to track renewals. Do not enter policy numbers.")
else:
    miss = []
    for _, r in df.iterrows():
        if r["renewal_date"] is None or str(r["renewal_date"]) == "NaT": miss.append(f"{r['type']}: renewal date missing")
        if not r["nominee_recorded"]: miss.append(f"{r['type']}: nominee not recorded")
        if not r["sum_assured"]: miss.append(f"{r['type']}: cover amount missing")
    if miss: st.warning("Missing information:\n\n" + "\n".join(f"- {m}" for m in miss))
have = set(df["type"].dropna()) if not df.empty else set()
for t in ["Health", "Term life", "Personal accident"]:
    if t not in have: st.info(f"No {t.lower()} policy recorded. Worth discussing with a qualified insurance professional if you have dependants or obligations.")
st.subheader("Questions to ask before buying or renewing")
st.markdown("- What is excluded, and what are the waiting periods?\n- What are the sub-limits, co-pay and claim process?\n- Is the premium fixed or can it change?\n- What happens if I miss a renewal?\n- Who is my nominee and are the details current?\n- Does my employer cover end when I change jobs?")
with st.expander("Plain-language terms"):
    st.markdown("**Sum assured:** amount paid on a claim.\n\n**Premium:** what you pay for cover.\n\n**Waiting period:** time before certain claims are covered.\n\n**Exclusion:** situations the policy does not cover.\n\n**Nominee:** person who receives the benefit.\n\n**Co-pay:** share of the bill you pay.")
st.caption("Check the policy wording and insurer details with IRDAI (irdai.gov.in). MoneyLife does not sell or recommend insurance.")
disclosure()
