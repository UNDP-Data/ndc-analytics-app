"""
Form elements fo building UI.
"""

import streamlit as st

from src import callbacks

from . import inputs

__all__ = ["add_search_form", "add_ask_form"]


def add_search_form():
    """
    Add a search form for full-text and vector search.

    Returns
    -------
    None
        Form is displayed in the app where it is called.
    """
    with st.form(key="search"):
        inputs.add_engine_select()
        inputs.add_query_text()
        inputs.add_geography_select()
        inputs.add_version_select()
        inputs.add_category_select()
        inputs.add_date_slider()
        st.form_submit_button(
            label="Search",
            help="Click to search",
            on_click=callbacks.search,
            type="primary",
        )


@st.fragment
def add_ask_form():
    """
    Add a simplified form for search in the ask page.

    This uses a container element instead of `st.form` to
    avoid having to insert `st.form_submit_button` and instead
    rely on user sending a message to trigger RAG.

    Returns
    -------
    None
        Form is displayed in the app where it is called.
    """
    with st.container(border=False):
        inputs.add_geography_select()
        inputs.add_version_select()
        inputs.add_category_select()
        inputs.add_date_slider()
