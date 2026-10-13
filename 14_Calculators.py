import pandas as pd, plotly.graph_objects as go, streamlit as st
from components.styling import page_header, disclosure, explain
from services import calculators as c
from utils.currency import format_inr
from utils.exports import df_to_csv_bytes

page_header("Financial Calculators", "Every rate is an editable assumption, never a promise.")
kind = st.selectbox("Calculator", ["SIP", "Lump-sum growth", "Simple interest", "Inflation and purchasing power", "EMI and amortization", "Fixed deposit", "Recurring deposit",
                                   "Education cost", "Home down payment", "Savings rate", "Emergency fund"])
N = st.number_input
res = {}
if kind == "SIP":
    m = N("Monthly investment (INR)", min_value=0.0, value=10000.0, step=500.0); r = N("Assumed annual return (%)", min_value=0.0, value=10.0); y = N("Years", min_value=1, value=15)
    fv = c.sip_fv(m, r, int(y) * 12); res = {"Invested": m * y * 12, "Estimated value": fv}
    st.plotly_chart(go.Figure(go.Scatter(y=c.project_series(0, m, r, int(y) * 12), line_color="#0F8B8D")).update_layout(title="Projected value by month", height=300), width="stretch")
elif kind == "Lump-sum growth":
    p = N("Amount (INR)", min_value=0.0, value=100000.0, step=5000.0); r = N("Assumed annual return (%)", min_value=0.0, value=8.0); y = N("Years", min_value=0.0, value=10.0)
    res = {"Estimated value": c.lump_sum_fv(p, r, y)}
elif kind == "Simple interest":
    p = N("Principal (INR)", min_value=0.0, value=100000.0, step=5000.0); r = N("Annual rate (%)", min_value=0.0, value=7.0); y = N("Years", min_value=0.0, value=3.0)
    res = {"Interest": c.simple_interest(p, r, y)}
elif kind == "Inflation and purchasing power":
    a = N("Amount today (INR)", min_value=0.0, value=100000.0, step=5000.0); i = N("Inflation (% a year)", min_value=0.0, value=6.0); y = N("Years", min_value=0.0, value=10.0)
    res = {"Same purchase will cost": c.inflate(a, i, y), "Today's purchasing power of the amount after those years": c.real_value(a, i, y)}
elif kind == "EMI and amortization":
    p = N("Principal (INR)", min_value=0.0, value=1000000.0, step=10000.0); r = N("Annual rate (%)", min_value=0.0, value=9.0); n = N("Tenure (months)", min_value=1, value=120)
    sch = c.amortization_schedule(p, r, int(n)); res = {"EMI": c.emi(p, r, int(n)), "Total interest": sum(x["interest"] for x in sch)}
    st.dataframe(pd.DataFrame(sch).round(2), width="stretch")
elif kind == "Fixed deposit":
    p = N("Deposit (INR)", min_value=0.0, value=100000.0, step=5000.0); r = N("Annual rate (%)", min_value=0.0, value=7.0); y = N("Years", min_value=0.0, value=3.0)
    res = {"Estimated maturity": c.fd_maturity(p, r, y)}; st.caption("Assumes quarterly compounding. Banks differ; check your deposit terms.")
elif kind == "Recurring deposit":
    m = N("Monthly deposit (INR)", min_value=0.0, value=5000.0, step=500.0); r = N("Annual rate (%)", min_value=0.0, value=6.5); n = N("Months", min_value=1, value=36)
    res = {"Deposited": m * n, "Estimated maturity": c.rd_maturity(m, r, int(n))}
elif kind == "Education cost":
    cost = N("Cost today (INR)", min_value=0.0, value=1500000.0, step=50000.0); i = N("Education cost inflation (% a year)", min_value=0.0, value=8.0); y = N("Years until needed", min_value=0.0, value=10.0)
    res = {"Estimated future cost": c.inflate(cost, i, y)}
elif kind == "Home down payment":
    pr = N("Home price today (INR)", min_value=0.0, value=8000000.0, step=100000.0); pc = N("Down payment (%)", min_value=0.0, max_value=100.0, value=20.0)
    ph = N("Price growth (% a year)", min_value=0.0, value=5.0); y = N("Years to buy", min_value=1, value=5); sv = N("Savings set aside (INR)", min_value=0.0, step=10000.0); g = N("Growth on savings (% a year)", min_value=0.0, value=7.0)
    dp = c.inflate(pr, ph, y) * pc / 100; res = {"Future down payment": dp, "Monthly saving needed": c.required_monthly(dp, sv, g, int(y) * 12)}
elif kind == "Savings rate":
    inc = N("Monthly income (INR)", min_value=0.0, step=1000.0); sp = N("Monthly spending incl. EMIs (INR)", min_value=0.0, step=1000.0)
    if inc == 0: st.info("Enter income above zero to calculate the rate.")
    else: st.metric("Savings rate", f"{(inc - sp) / inc:.1%}"); res = {"Savings rate (%)": (inc - sp) / inc * 100}
else:
    e = N("Essential monthly expenses (INR)", min_value=0.0, value=40000.0, step=1000.0); mths = N("Months of cover", min_value=1, value=6); res = {"Target fund": e * mths}
for k, v in res.items():
    st.metric(k, f"{v:.1f}%" if "%" in k else format_inr(v))
if res: st.download_button("Download result (CSV)", df_to_csv_bytes(pd.DataFrame([res])), "result.csv", "text/csv")
st.caption("For tax estimates, use the Tax Planning page, where the rules are editable and must be verified.")
explain("SIP: m x ((1+r)^n - 1)/r, r = annual/12, month-end contributions. Lump sum: P x (1+r)^(12y). Simple interest: P x rate x years. Inflation: A x (1+i)^y. EMI: P x r x (1+r)^n / ((1+r)^n - 1). FD: P x (1 + rate/4)^(4y). RD: each deposit compounds quarterly until maturity. Values are unrounded internally and rounded to whole rupees for display. All are estimates.")
disclosure()
