from datetime import date
import plotly.express as px, streamlit as st
from components.styling import page_header, disclosure
from services.net_worth import summarize
from utils.currency import format_inr
from utils.exports import df_to_csv_bytes
from utils.state import get_table

page_header("Family Money Map", "A manual inventory of what you own and owe. Values are your own estimates.")
CATS = ["Savings and cash", "FD / RD", "EPF / PPF", "Mutual funds and shares", "Gold", "Property", "Other asset", "Home loan", "Other loan", "Credit card"]
df = get_table("money_map", {"name": "object", "kind": "object", "category": "object", "value": "float64", "last_updated": "datetime64[ns]", "nominee_reviewed": "bool"})
df = st.data_editor(df, num_rows="dynamic", width="stretch", key="mm_ed", column_config={
    "kind": st.column_config.SelectboxColumn("Asset or liability", options=["Asset", "Liability"]), "category": st.column_config.SelectboxColumn(options=CATS),
    "value": st.column_config.NumberColumn("Value (INR, your estimate)", min_value=0.0), "last_updated": st.column_config.DateColumn("Last updated"),
    "nominee_reviewed": st.column_config.CheckboxColumn("Nominee reviewed")})
st.session_state["money_map"] = df
if df.empty: st.info("Add your first asset or loan above. Do not enter account numbers or passwords.")
else:
    s = summarize(df, date.today()); m = st.columns(3)
    m[0].metric("Assets", format_inr(s["assets"])); m[1].metric("Liabilities", format_inr(s["liabilities"])); m[2].metric("Estimated net worth", format_inr(s["net_worth"]))
    st.plotly_chart(px.bar(s["by_category"], x="category", y="value", color="kind", title="Breakdown", color_discrete_map={"Asset": "#0F8B8D", "Liability": "#12284C"}), width="stretch")
    if len(s["stale"]): st.warning(f"{len(s['stale'])} record(s) are missing a date or were updated over 180 days ago."); st.dataframe(s["stale"][["name", "category", "last_updated"]])
    st.download_button("Export summary (CSV)", df_to_csv_bytes(df), "money_map.csv", "text/csv")
st.subheader("Document checklist")
for i, d in enumerate(["Bank account and nominee details", "Insurance policy documents", "Loan statements", "Investment statements", "PAN and Aadhaar copies kept safely (do not upload here)", "Will or nomination records", "Property papers", "Last filed tax return"]):
    st.checkbox(d, key=f"doc_{i}")
disclosure()
