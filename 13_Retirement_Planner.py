import pandas as pd, plotly.graph_objects as go, streamlit as st
from components.styling import page_header, disclosure, explain
from services import calculators as c
from services.retirement import project
from utils.currency import format_inr

page_header("Retirement Planner", "An educational estimate. Change the assumptions and watch the result move.")
a, b, c3 = st.columns(3)
age = a.number_input("Current age", 18, 80, 30); ra = b.number_input("Retirement age", 19, 90, 60); dur = c3.number_input("Years in retirement to fund", 5, 50, 25)
cur = a.number_input("Retirement savings now (INR)", min_value=0.0, step=10000.0); mo = b.number_input("Monthly contribution (INR)", min_value=0.0, step=1000.0)
ex = c3.number_input("Monthly expenses in today's money (INR)", min_value=0.0, value=50000.0, step=1000.0)
pen = a.number_input("Expected pension, today's money (INR/month)", min_value=0.0)
inf = b.slider("Inflation (% a year)", 0.0, 12.0, 6.0, 0.5); gr = c3.slider("Growth before retirement (% a year, illustrative)", 0.0, 15.0, 9.0, 0.5)
post = a.slider("Return after retirement (% a year, illustrative)", 0.0, 12.0, 7.0, 0.5)
try: r = project(int(age), int(ra), cur, mo, ex, inf, gr, post, int(dur), pen)
except ValueError as e: st.error(str(e)); st.stop()
m = st.columns(4)
m[0].metric("Years to retirement", r["years"]); m[1].metric("Future monthly expense", format_inr(r["future_monthly_expense"]))
m[2].metric("Corpus estimate", format_inr(r["corpus_needed"])); m[3].metric("Funding gap" if r["gap"] > 0 else "Surplus", format_inr(abs(r["gap"])))
st.write(f"Projected savings: **{format_inr(r['projected'])}** nominal, about **{format_inr(r['projected_real'])}** in today's purchasing power. Monthly contribution that would close the gap: **{format_inr(r['required_monthly'])}**.")
s = c.project_series(cur, mo, gr, r["years"] * 12)
st.plotly_chart(go.Figure(go.Scatter(x=[i / 12 for i in range(1, len(s) + 1)], y=s, line_color="#0F8B8D")).update_layout(title="Projected savings (nominal)", xaxis_title="Years", height=320), width="stretch")
st.subheader("Sensitivity: funding gap (INR)")
rows = {f"growth {g}%": {f"inflation {i}%": format_inr(project(int(age), int(ra), cur, mo, ex, i, g, post, int(dur), pen)["gap"]) for i in (4, 6, 8)} for g in (6, 9, 12)}
st.dataframe(pd.DataFrame(rows).T, width="stretch")
explain("Future expense = today's expense x (1+inflation)^years. Corpus = present value at retirement of monthly needs (net of inflated pension) over the chosen years, discounted at the real rate. Savings projected with monthly compounding, contributions at month end. Nominal = rupee amounts in the future; today's purchasing power = nominal / (1+inflation)^years. None of this is guaranteed.")
disclosure()
