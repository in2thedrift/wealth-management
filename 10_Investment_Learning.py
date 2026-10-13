import streamlit as st
from components.styling import page_header, disclosure
from data.content import TOPICS, SRC

page_header("Investment Learning Centre", "Plain-language lessons. General education only; no stock tips or personal recommendations.")
level = st.radio("Level", ["All", "Beginner", "Intermediate", "Advanced"], horizontal=True)
keys = [k for k, t in TOPICS.items() if level == "All" or t["level"] == level]
if not keys: st.info("No lessons at this level yet."); st.stop()
k = st.selectbox("Topic", keys, format_func=lambda k: TOPICS[k]["title"]); t = TOPICS[k]
st.header(t["title"]); st.caption(t["level"])
st.write(t["explain"]); st.markdown(f"**Indian example:** {t['example']}")
a, b = st.columns(2); a.success(f"**Benefits:** {t['benefits']}"); b.warning(f"**Risks:** {t['risks']}")
st.markdown(f"**Common misconception:** {t['myths']}")
with st.expander("Glossary"):
    for term, d in t["glossary"].items(): st.markdown(f"**{term}:** {d}")
st.subheader("Quick quiz")
for i, (q, opts, ans) in enumerate(t["quiz"]):
    pick = st.radio(q, opts, index=None, key=f"q_{k}_{i}")
    if pick is not None: st.success("Correct.") if opts.index(pick) == ans else st.error("Not quite. Re-read the lesson and try again.")
st.subheader("Official sources")
for s in t["sources"]: st.markdown(f"- [{SRC[s][0]}]({SRC[s][1]})")
st.caption("Rates and rules change. Check the official site for current details.")
disclosure()
