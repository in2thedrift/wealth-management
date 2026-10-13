import streamlit as st
from components.styling import page_header
from config import BRAND_NAME
from utils.exports import session_to_json
from utils.state import TABLE_KEYS

page_header("Profile, Privacy and Settings", "You control what is stored, and you can erase it.")
st.markdown(f"**How {BRAND_NAME} handles your data:** everything lives in this browser session's memory only. It is not saved to a database, is cleared when the session ends, and demo data is kept separate from yours. Do not enter passwords, OTPs or card codes anywhere.")
tabs = {k: st.session_state[k] for k in TABLE_KEYS if k in st.session_state}
st.write(f"Tables held in this session: {', '.join(tabs) or 'none'}")
if tabs: st.download_button("Export all my data (JSON)", session_to_json(tabs), "moneylife_export.json", "application/json")
if st.button("Delete all my data from this session", type="primary"):
    for k in list(st.session_state.keys()): del st.session_state[k]
    st.success("Deleted."); st.rerun()
st.caption("Login and permanent storage are not implemented yet. Add a vetted authentication provider and security review before storing real user data.")
