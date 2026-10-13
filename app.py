"""MoneyLife entry point. Run: streamlit run app.py"""
from pathlib import Path
import streamlit as st
from config import BRAND_NAME, BRAND_SUBTITLE

st.set_page_config(page_title=f"{BRAND_NAME} - {BRAND_SUBTITLE}", page_icon=":material/account_balance:", layout="wide")

ROOT = Path(__file__).parent
SECTIONS = {
    "Overview": [("01_Home", "Home Dashboard", "home"), ("02_Financial_Health", "Financial Health Passport", "monitor_heart"), ("19_My_Financial_Plan", "My Financial Plan", "assignment")],
    "Money": [("03_Salary_Planner", "Salary-to-Security Planner", "payments"), ("04_Budget_Manager", "Budget and Expense Manager", "receipt_long"),
              ("09_Leakage_Audit", "Financial Leakage Audit", "search"), ("08_Family_Money_Map", "Family Money Map", "account_tree")],
    "Plan": [("05_Emergency_Fund", "Emergency Fund Simulator", "shield"), ("06_Debt_Planner", "Debt and EMI Planner", "credit_score"),
             ("07_Goal_Planner", "Life-Goal Reality Checker", "flag"), ("13_Retirement_Planner", "Retirement Planner", "beach_access"),
             ("11_Tax_Planner", "Tax Planning and Calendar", "request_quote"), ("12_Insurance_Checklist", "Insurance and Protection", "health_and_safety")],
    "Learn and tools": [("10_Investment_Learning", "Investment Learning Centre", "school"), ("14_Calculators", "Financial Calculators", "calculate"),
                        ("15_Financial_Calendar", "Personal Finance Calendar", "event"), ("16_Language_Centre", "Finance in Your Language", "translate")],
    "Household and help": [("17_Family_Mode", "Family Finance Mode", "family_restroom"), ("18_Expert_Help", "Expert Help Marketplace", "support_agent")],
    "Account": [("20_Settings", "Profile, Privacy and Settings", "settings"), ("21_About", "About and Disclosures", "info")],
}

missing = [f"pages/{f}.py" for items in SECTIONS.values() for f, _, _ in items if not (ROOT / "pages" / f"{f}.py").is_file()]
if missing:
    st.error("Some page files are missing from your repository, so the app cannot start.")
    st.write("Each file must sit in a folder named `pages` next to `app.py`, with exactly this name (case-sensitive, underscores, no spaces):")
    st.code("\n".join(missing))
    st.write("Files found next to app.py:")
    st.code("\n".join(sorted(p.name for p in ROOT.iterdir())))
    st.stop()

pages, first = {}, True
for section, items in SECTIONS.items():
    pages[section] = []
    for f, title, icon in items:
        pages[section].append(st.Page(f"pages/{f}.py", title=title, icon=f":material/{icon}:", default=first))
        first = False
st.navigation(pages).run()
