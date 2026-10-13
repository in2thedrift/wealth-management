"""MoneyLife entry point. Run: streamlit run app.py"""
import streamlit as st
from config import BRAND_NAME, BRAND_SUBTITLE

st.set_page_config(page_title=f"{BRAND_NAME} - {BRAND_SUBTITLE}", page_icon=":material/account_balance:", layout="wide")
P = lambda f, t, i, **k: st.Page(f"pages/{f}.py", title=t, icon=f":material/{i}:", **k)
pages = {
    "Overview": [P("01_Home", "Home Dashboard", "home", default=True), P("02_Financial_Health", "Financial Health Passport", "monitor_heart"),
                 P("19_My_Financial_Plan", "My Financial Plan", "assignment")],
    "Money": [P("03_Salary_Planner", "Salary-to-Security Planner", "payments"), P("04_Budget_Manager", "Budget and Expense Manager", "receipt_long"),
              P("09_Leakage_Audit", "Financial Leakage Audit", "search"), P("08_Family_Money_Map", "Family Money Map", "account_tree")],
    "Plan": [P("05_Emergency_Fund", "Emergency Fund Simulator", "shield"), P("06_Debt_Planner", "Debt and EMI Planner", "credit_score"),
             P("07_Goal_Planner", "Life-Goal Reality Checker", "flag"), P("13_Retirement_Planner", "Retirement Planner", "beach_access"),
             P("11_Tax_Planner", "Tax Planning and Calendar", "request_quote"), P("12_Insurance_Checklist", "Insurance and Protection", "health_and_safety")],
    "Learn and tools": [P("10_Investment_Learning", "Investment Learning Centre", "school"), P("14_Calculators", "Financial Calculators", "calculate"),
                        P("15_Financial_Calendar", "Personal Finance Calendar", "event"), P("16_Language_Centre", "Finance in Your Language", "translate")],
    "Household and help": [P("17_Family_Mode", "Family Finance Mode", "family_restroom"), P("18_Expert_Help", "Expert Help Marketplace", "support_agent")],
    "Account": [P("20_Settings", "Profile, Privacy and Settings", "settings"), P("21_About", "About and Disclosures", "info")],
}
st.navigation(pages).run()
