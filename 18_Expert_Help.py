import streamlit as st
from components.styling import page_header, disclosure

page_header("Expert Help Marketplace", "A preview of how professional listings will look.")
st.warning("DEMO LISTINGS ONLY. These are fictional and carry no real credentials. No bookings or payments are possible, and MoneyLife does not execute trades, hold client money or give paid investment advice.")
DEMO = [dict(name="Demo Planner A", cat="Financial planning education", quals="(Fictional)", reg="Not applicable (demo)", fees="Rs 0 (demo)", scope="General education only", conflict="None (demo)"),
        dict(name="Demo Advisor B", cat="Qualified investment-advisory services", quals="(Fictional)", reg="Registration must be verified before any real listing", fees="Fixed fee (demo)", scope="Would require appropriate SEBI permissions", conflict="Disclosure required"),
        dict(name="Demo Tax Consultant C", cat="Tax consultation", quals="(Fictional)", reg="Verify professional membership", fees="Hourly (demo)", scope="Tax questions only", conflict="None (demo)"),
        dict(name="Demo Insurance Guide D", cat="Insurance guidance", quals="(Fictional)", reg="Verify IRDAI-linked licence", fees="Fee or commission must be disclosed", scope="Explaining policy terms", conflict="Commission disclosure required")]
cat = st.selectbox("Category", ["All"] + sorted({d["cat"] for d in DEMO}))
for d in DEMO:
    if cat in ("All", d["cat"]):
        with st.container(border=True):
            st.subheader(d["name"]); st.caption(d["cat"])
            st.markdown(f"**Qualifications:** {d['quals']}  \n**Registration:** {d['reg']}  \n**Fees:** {d['fees']}  \n**Scope and limits:** {d['scope']}  \n**Conflicts of interest:** {d['conflict']}")
            st.button("Booking not available", disabled=True, key=d["name"])
disclosure()
