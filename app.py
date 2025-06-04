"""
Entry point to NDC Analytics application.
"""

import st_undp
import streamlit as st
from dotenv import load_dotenv

from src import components
from src import database as db
from src import utils

load_dotenv()


st_undp.apply_style(title="NDC Analytics App")

if "date_range" not in st.session_state:
    metadata = db.get_metadata()
    st.session_state.update(metadata)

if "feed" not in st.session_state:
    st.session_state["feed"] = utils.get_feed()

if "history" not in st.session_state:
    st.session_state["history"] = []

pages = [
    st.Page(page="src/pages/search.py", url_path="./"),
    st.Page(page="src/pages/ask.py", url_path="/ask"),
    st.Page(page="src/pages/ndcs.py", url_path="/ndcs"),
    st.Page(page="src/pages/rss.py", url_path="/rss"),
    st.Page(page="src/pages/about.py", url_path="/about"),
]

st_undp.header(
    title="DFx AI as a Service".upper(),
    subtitle="NDC Analytics App",
    title_href="https://data.undp.org/what-we-do/ai-as-service",
    subtitle_href="./",
    pages=pages,
    logo="undp",
)
st.subheader("Intelligent multi-lingual search across the NDC registry")
pg = st.navigation(pages=pages, position="hidden")
st_undp.breadcrumb({"Home": "/", pg.title: None})
with st.sidebar:
    if "search" in pg.title.lower():
        components.add_search_form()
    elif "ask" in pg.title.lower():
        components.add_ask_form()
pg.run()
