from datetime import date
import pandas as pd, streamlit as st
from components.styling import page_header, disclosure, explain
from services.tax_estimation import total_tax
from utils.currency import format_inr
from utils.dates import financial_year, assessment_year

page_header("Tax Planning and Tax Calendar", "Educational estimates only. Tax rules change; verify at incometax.gov.in.")
st.error("DEMONSTRATION: the slabs below are placeholders that YOU must replace with figures verified from the Income Tax Department for your financial year. This tool does not claim they are current.")
fy_now = financial_year(date.today()); fys = [f"{y}-{str(y + 1)[-2:]}" for y in range(2023, date.today().year + 2)]
fy = st.selectbox("Financial year", fys, index=fys.index(fy_now) if fy_now in fys else 0); st.caption(f"Assessment year: {assessment_year(fy)}")
regime = st.radio("Regime to model", ["New regime", "Old regime"], horizontal=True)
st.markdown("**Slabs for the selected year and regime** (blank upper limit = no limit)")
demo = pd.DataFrame({"upper_limit": [400000.0, 800000.0, None], "rate_pct": [0.0, 5.0, 10.0]})
slabs_df = st.data_editor(demo, num_rows="dynamic", width="stretch", key=f"slabs_{fy}_{regime}")
a, b, c = st.columns(3)
gross = a.number_input("Salary / income (INR a year)", min_value=0.0, step=10000.0); std = b.number_input("Standard deduction (INR)", min_value=0.0)
ded = c.number_input("Other eligible deductions (INR)", min_value=0.0, help="Only if your selected regime allows them.")
cess = a.number_input("Cess (%)", min_value=0.0, value=4.0); rl = b.number_input("Rebate applies if income up to (INR)", min_value=0.0); rm = c.number_input("Maximum rebate (INR)", min_value=0.0)
try:
    sl = [(None if pd.isna(u) else float(u), float(r)) for u, r in zip(slabs_df["upper_limit"], slabs_df["rate_pct"])]
    taxable = max(gross - std - ded, 0.0); r = total_tax(taxable, sl, cess, rl, rm)
    m = st.columns(4); m[0].metric("Taxable income", format_inr(taxable)); m[1].metric("Slab tax", format_inr(r["slab_tax"])); m[2].metric("Rebate", format_inr(r["rebate"])); m[3].metric("Estimated total", format_inr(r["total"]))
except ValueError as e: st.error(str(e))
explain("Slab tax is calculated progressively. Rebate = min(tax, maximum rebate) if taxable income is within the limit. Total = (tax - rebate) x (1 + cess). Surcharge, capital gains, special rates and other income types are NOT modelled.")
st.subheader("Typical calendar (verify exact dates on incometax.gov.in)")
st.table(pd.DataFrame({"Item": ["Advance tax instalments", "Income tax return filing", "Investment proofs to employer", "Form 16 / tax statements"], "Commonly around": ["15 Jun, 15 Sep, 15 Dec, 15 Mar", "31 July for many individuals", "Early in the year, per employer", "After year end"]}))
st.subheader("Document checklist")
for i, d in enumerate(["Form 16", "Form 26AS / AIS", "Bank interest certificates", "Investment and insurance proofs", "Rent receipts and landlord details", "Home loan interest certificate", "Capital gains statements"]): st.checkbox(d, key=f"tx_{i}")
st.subheader("Questions for a qualified tax professional")
st.markdown("- Which regime suits my situation?\n- Which deductions apply to me?\n- How are my other incomes taxed?\n- Do I need to pay advance tax?\n- Are there any notices or mismatches to resolve?")
disclosure()
