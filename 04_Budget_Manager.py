import pandas as pd, plotly.express as px, streamlit as st
from components.styling import page_header, disclosure
from services import transaction_analysis as ta
from utils.exports import df_to_csv_bytes
from utils.state import get_table

page_header("Budget and Expense Manager", "Record transactions or import a CSV. No bank login needed.")
SCHEMA = {"date": "datetime64[ns]", "description": "object", "amount": "float64", "type": "object", "category": "object", "payment_method": "object"}
tx = get_table("txns", SCHEMA)
t_add, t_view, t_imp, t_sum = st.tabs(["Add", "View and edit", "Import CSV", "Summaries"])
with t_add:
    with st.form("add_tx", clear_on_submit=True):
        a, b = st.columns(2)
        d = a.date_input("Date"); desc = b.text_input("Description")
        amt = a.number_input("Amount (INR)", min_value=0.0, step=100.0); typ = b.selectbox("Type", ["Expense", "Income"])
        cat = a.text_input("Category (blank = auto)"); pm = b.selectbox("Payment method", ["UPI", "Card", "Cash", "Bank transfer", "Other"])
        if st.form_submit_button("Add transaction", type="primary"):
            if not desc.strip() or amt <= 0: st.error("Enter a description and an amount above zero.")
            else:
                row = pd.DataFrame([dict(date=pd.Timestamp(d), description=desc.strip(), amount=amt, type=typ, category=cat.strip() or ta.categorize(desc), payment_method=pm)])
                st.session_state["txns"] = pd.concat([tx, row], ignore_index=True); st.success("Added."); st.rerun()
with t_view:
    if tx.empty: st.info("No transactions yet. Add one or import a CSV.")
    else:
        q = st.text_input("Search description"); f1, f2 = st.columns(2)
        types = f1.multiselect("Type", ["Income", "Expense"], ["Income", "Expense"]); cats = f2.multiselect("Category", sorted(tx["category"].dropna().unique()))
        mask = tx["type"].isin(types) & tx["description"].str.contains(q, case=False, na=False)
        if cats: mask &= tx["category"].isin(cats)
        st.caption("Edit cells or select rows and press Delete. Edits apply to the visible (filtered) rows.")
        edited = st.data_editor(tx[mask], num_rows="dynamic", width="stretch", key="tx_ed",
            column_config={"date": st.column_config.DateColumn(), "type": st.column_config.SelectboxColumn(options=["Income", "Expense"])})
        if st.button("Save changes"):
            st.session_state["txns"] = pd.concat([tx[~mask], edited], ignore_index=True).sort_values("date"); st.rerun()
        if st.button("Auto-categorise uncategorised rows (simple keyword rules)"):
            u = tx["category"].isna() | (tx["category"] == "")
            tx.loc[u, "category"] = tx.loc[u, "description"].map(ta.categorize); st.session_state["txns"] = tx; st.rerun()
        st.download_button("Export filtered (CSV)", df_to_csv_bytes(tx[mask]), "transactions.csv", "text/csv")
with t_imp:
    st.caption("Required columns: date, description, amount. Optional: type (Income/Expense), category, payment_method. Max 2 MB and 5,000 rows.")
    up = st.file_uploader("Choose CSV", type=["csv"])
    if up is not None:
        if up.size > 2 * 1024 * 1024: st.error("File is larger than 2 MB.")
        else:
            try: raw = pd.read_csv(up)
            except Exception: st.error("Could not read this file as CSV."); raw = None
            if raw is not None:
                clean, errs = ta.clean_transactions(raw)
                if errs: st.warning(f"{len(errs)} problem(s) found. Invalid rows were rejected."); st.write("\n".join(errs[:15]))
                st.write(f"{len(clean)} valid rows ready."); st.dataframe(clean.head(20))
                if len(clean) and st.button("Import valid rows", type="primary"):
                    clean["category"] = clean["category"].fillna(clean["description"].map(ta.categorize))
                    st.session_state["txns"] = pd.concat([tx, clean], ignore_index=True); st.success("Imported."); st.rerun()
with t_sum:
    if tx.empty: st.info("Add transactions to see summaries.")
    else:
        ms = ta.monthly_summary(tx); st.plotly_chart(px.bar(ms, x="month", y=["Income", "Expense"], barmode="group", title="Income vs expenses by month", color_discrete_sequence=["#0F8B8D", "#12284C"]), width="stretch")
        ex = tx[tx["type"] == "Expense"]
        if not ex.empty: st.plotly_chart(px.pie(ex, names="category", values="amount", hole=0.5, title="Spending by category"), width="stretch")
        st.dataframe(ms.round(0), width="stretch")
        rec = ta.recurring(tx)
        if not rec.empty: st.subheader("Suspected recurring expenses"); st.dataframe(rec.round(0), width="stretch")
disclosure()
