import streamlit as st
from components.styling import page_header
from config import DISCLOSURE, REGULATORY_LAST_VERIFIED, BRAND_NAME

page_header("About, Methodology and Disclosures", f"How {BRAND_NAME} works and what it is not.")
st.markdown(DISCLOSURE)
st.subheader("Data and privacy")
st.markdown("This prototype keeps data in Streamlit session state only. It disappears when the session ends and is not secure permanent storage. We never ask for bank passwords, OTPs or card codes.")
st.subheader("Regulatory status")
st.warning(f"Last verified: {REGULATORY_LAST_VERIFIED}")
st.markdown("Before launch, confirm with qualified Indian counsel whether any planned feature (advice, distribution, insurance solicitation, data handling) needs SEBI, RBI, IRDAI or data-protection compliance.")
