"""Theme and shared page chrome."""
import streamlit as st
from config import BRAND_NAME, DISCLOSURE, NAVY, TEAL

CSS = f"""
<style>
h1, h2, h3 {{ color: {NAVY}; letter-spacing: -0.01em; }}
[data-testid="stMetric"] {{ background:#F6F9FA; border:1px solid #DCE6E8; border-left:4px solid {TEAL};
  padding:14px 16px; border-radius:8px; }}
.ml-note {{ font-size:0.9rem; color:#4A5A6A; }}
@media (max-width: 640px) {{ [data-testid="stMetricValue"] {{ font-size:1.3rem; }} }}
</style>"""


def page_header(title: str, subtitle: str) -> None:
    st.markdown(CSS, unsafe_allow_html=True)
    st.title(title)
    st.caption(subtitle)


def disclosure() -> None:
    st.divider()
    st.markdown(f"<p class='ml-note'>{DISCLOSURE}</p>", unsafe_allow_html=True)


def explain(text: str) -> None:
    with st.expander("Formula, assumptions and limits"):
        st.markdown(text)
