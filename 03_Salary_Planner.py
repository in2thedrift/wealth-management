import pandas as pd, plotly.graph_objects as go, streamlit as st
from components.styling import page_header, disclosure, explain
from services.budgeting import summarize, example_budgets, extra_saving_effect
from utils.currency import format_inr
from utils.exports import df_to_csv_bytes
from utils.state import get_table

page_header("Salary-to-Security Planner", "Allocate your take-home pay across needs, EMIs and savings.")
CATS = ["Housing", "Food and groceries", "Transport", "Utilities", "Healthcare", "Family contributions", "Education", "EMIs and debt", "Insurance premiums", "Discretionary"]
df = get_table("salary_budget", {"Category": "object", "Current": "float64", "Proposed": "float64"}, [dict(Category=c, Current=0.0, Proposed=0.0) for c in CATS])
a, b, c3 = st.columns(3)
income = a.number_input("Monthly take-home income (INR)", min_value=0.0, step=1000.0)
target = b.number_input("Monthly savings target (INR)", min_value=0.0, step=500.0)
saved = c3.number_input("Current savings (INR)", min_value=0.0, step=5000.0)
st.caption("Edit amounts or add your own categories. Changes stay for this session.")
df = st.data_editor(df, num_rows="dynamic", width="stretch", key="sal_ed",
    column_config={"Current": st.column_config.NumberColumn(min_value=0.0, format="%.0f"), "Proposed": st.column_config.NumberColumn(min_value=0.0, format="%.0f")})
df = df.fillna({"Category": "Other", "Current": 0.0, "Proposed": 0.0}); st.session_state["salary_budget"] = df
cur = summarize(income, dict(zip(df["Category"], df["Current"])), target)
pro = summarize(income, dict(zip(df["Category"], df["Proposed"])), target)
m = st.columns(4)
m[0].metric("Spending now", format_inr(cur["total_expenses"])); m[1].metric("Left each month", format_inr(cur["remaining"]))
m[2].metric("Left (proposed)", format_inr(pro["remaining"])); m[3].metric("Left per year", format_inr(cur["annual_remaining"]))
if cur["overspend"]: st.error("Your current spending is higher than your income. Review the largest categories first; keep paying required EMIs.")
if target and not cur["target_feasible"]:
    st.warning(f"Your target of {format_inr(target)} is more than the {format_inr(cur['max_feasible_saving'])} currently available.")
fig = go.Figure([go.Bar(name="Current", x=df["Category"], y=df["Current"], marker_color="#12284C"), go.Bar(name="Proposed", x=df["Category"], y=df["Proposed"], marker_color="#0F8B8D")])
fig.update_layout(barmode="group", height=340, margin=dict(t=20)); st.plotly_chart(fig, width="stretch")
st.subheader("Effect of saving a little more")
x1, x2, x3 = st.columns(3)
extra = x1.number_input("Extra saving per month (INR)", min_value=0.0, value=2000.0, step=500.0)
rate = x2.number_input("Illustrative annual growth (%)", min_value=0.0, value=6.0)
yrs = x3.number_input("Years", min_value=1, value=5)
e = extra_saving_effect(extra, rate, int(yrs)); st.write(f"Contributed {format_inr(e['contributed'])}; estimated value {format_inr(e['estimated_value'])} (not guaranteed).")
st.subheader("Educational examples (not advice)")
ex = pd.DataFrame(example_budgets(income, cur["total_expenses"] - float(df.loc[df["Category"] == "Discretionary", "Current"].sum())))
if income: st.dataframe(ex.round(0), width="stretch"); st.caption("Savings are capped by what remains after your obligations. Households differ; there is no single right split.")
st.download_button("Download budget (CSV)", df_to_csv_bytes(df), "budget.csv", "text/csv")
explain("Remaining = income - total of categories. Annual = monthly x 12. Examples: savings = min(percentage x income, income left after non-discretionary spending).")
disclosure()
