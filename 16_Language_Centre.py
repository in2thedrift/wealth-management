import streamlit as st
from components.styling import page_header, disclosure
from data.content import TOPICS

page_header("Finance in Your Language", "Simple explanations by level. Reviewed translations will be added over time.")
TRANSLATIONS = {"en": {}, "hi": {}}  # add reviewed {"Term": "translation"} pairs here, per language
lang = st.selectbox("Language", ["English", "Hindi (reviewed translations coming)"])
if lang.startswith("Hindi") and not TRANSLATIONS["hi"]:
    st.info("Reviewed Hindi translations are not available yet. Showing English so nothing is mistranslated.")
level = st.radio("Level", ["Beginner", "Intermediate", "Advanced"], horizontal=True)
shown = False
for t in TOPICS.values():
    if t["level"] != level: continue
    for term, d in t["glossary"].items():
        shown = True; st.markdown(f"**{term}:** {d}  \n*Example: {t['example']}*")
if not shown: st.write("No terms at this level yet.")
st.caption("Formulas, numbers and regulatory disclosures stay identical across languages.")
disclosure()
