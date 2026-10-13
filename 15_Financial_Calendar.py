from datetime import date
import streamlit as st
from components.styling import page_header, disclosure
from utils.exports import df_to_csv_bytes
from utils.state import get_table

page_header("Personal Finance Calendar", "Your reminders live here. MoneyLife does not send emails, SMS or WhatsApp messages.")
CATS = ["EMI due", "Insurance renewal", "Tax documents", "Goal review", "Budget review", "Emergency fund review", "Learning", "Retirement review", "Document update"]
df = get_table("tasks", {"task": "object", "category": "object", "due": "datetime64[ns]", "done": "bool"})
df = st.data_editor(df, num_rows="dynamic", width="stretch", key="task_ed", column_config={
    "category": st.column_config.SelectboxColumn(options=CATS), "due": st.column_config.DateColumn("Due date"), "done": st.column_config.CheckboxColumn("Done")})
st.session_state["tasks"] = df
if df.empty: st.info("Add a task above, for example an EMI due date."); st.stop()
today = date.today(); d = df.dropna(subset=["due"]).copy(); d["due_d"] = d["due"].dt.date
over = d[(~d["done"]) & (d["due_d"] < today)]
if len(over): st.error(f"{len(over)} overdue task(s)"); st.dataframe(over[["task", "category", "due"]], width="stretch")
f = st.multiselect("Filter category", CATS)
up = d[(~d["done"]) & (d["due_d"] >= today)]
if f: up = up[up["category"].isin(f)]
st.subheader("Upcoming"); st.dataframe(up.sort_values("due")[["task", "category", "due"]], width="stretch")
st.download_button("Export tasks (CSV)", df_to_csv_bytes(df), "tasks.csv", "text/csv")
disclosure()
