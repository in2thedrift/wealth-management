import streamlit as st
from components.styling import page_header, disclosure, explain
from services.goals import project
from utils.currency import format_inr

page_header("Life-Goal Reality Checker", "See what a goal may cost and whether your plan reaches it.")
a, b = st.columns(2)
name = a.text_input("Goal name", "Child's education")
cost = b.number_input("Cost today (INR)", min_value=0.0, value=2500000.0, step=50000.0)
yrs = a.number_input("Years to goal", min_value=0.5, value=12.0, step=0.5)
ex = b.number_input("Savings set aside (INR)", min_value=0.0, value=200000.0, step=10000.0)
mo = a.number_input("Monthly contribution (INR)", min_value=0.0, value=15000.0, step=1000.0)
inf = b.slider("Inflation assumption (% a year)", 0.0, 12.0, 6.0, 0.5)
gr = a.slider("Illustrative growth assumption (% a year, not guaranteed)", 0.0, 15.0, 8.0, 0.5)
try:
    r = project(cost, yrs, inf, ex, mo, gr)
except ValueError as e:
    st.error(str(e)); st.stop()
c = st.columns(4)
c[0].metric("Future cost", format_inr(r["future_cost"]))
c[1].metric("Projected savings", format_inr(r["projected"]))
c[2].metric("Shortfall" if r["gap"] > 0 else "Surplus", format_inr(abs(r["gap"])))
c[3].metric("Monthly needed", format_inr(r["required_monthly"]))
st.subheader("Alternatives")
alts = {"Current plan": (yrs, mo, cost), "Contribute 25% more": (yrs, mo * 1.25, cost),
        "Two years later": (yrs + 2, mo, cost), "Goal 20% cheaper": (yrs, mo, cost * 0.8)}
st.dataframe([{"Scenario": k, "Gap (INR)": format_inr(project(v[2], v[0], inf, ex, v[1], gr)["gap"])} for k, v in alts.items()], width="stretch")
explain("Future cost = cost x (1+inflation)^years. Projected = savings x (1+r)^n + monthly x ((1+r)^n - 1)/r, with r = growth/12 (zero growth handled separately). Growth is illustrative, never guaranteed.")
disclosure()
