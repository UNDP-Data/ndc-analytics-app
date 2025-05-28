"""
Input elements fo building UI.
"""

from random import choice

import streamlit as st

from src import callbacks
from src.entities import Engine
from src.utils import read_csv_file

__all__ = [
    "add_engine_select",
    "add_query_text",
    "add_geography_select",
    "add_version_select",
    "add_category_select",
    "add_date_slider",
    "add_view_control",
    "add_ndc_select",
    "add_globe_toggle",
    "add_chat_input",
]


def add_engine_select():
    """
    Add a select box for choosing a search engine.

    Returns
    -------
    None
        Selectbox is displayed in the app where it is called.
    """
    st.selectbox(
        label="Search Engine",
        options=Engine,
        index=0,
        key="engine",
        help="""Select a search engine to use. Full-text search gives you better control
        over what terms need to appear in your documents but cannot handle synonyms and
        subtle contextual nuances. It also requires  you to specify the language of your
        query. Vector search can match texts in any supported language and return you
        relevant documents even if they don't contain your query terms but is semantically
        similar.""",
        placeholder="Choose an option",
    )


def add_query_text():
    """
    Add a text area for inputting a search query.

    Returns
    -------
    None
        Text area is displayed in the app where it is called.
    """
    placeholders = [
        "climate change mitigation and adaptation measures",
        "electric and hybrid bus systems",
        "emission of greenhouse gases",
        "nature-based solutions",
    ]
    st.text_area(
        label="Query",
        value=st.session_state.get("query", ""),
        height=None,
        max_chars=256,
        key="query",
        help="""Enter the text you want to search for. The query is case insensitive.
        By default, the search engine will interpret the terms in your query using
        the OR operator, meaning it will find the documents containing any of the terms.
        If you want to search for an exact phrase, enclose your query into double quotes ("").
        If you want to exclude texts that contain certain terms, prefix such terms with a minus sign (-).
        For a detailed explanation and examples of queries, see the [query guide](./about#query-guide).
        """,
        placeholder=choice(placeholders),
    )


def add_geography_select():
    """
    Add a select box for choosing a geographical scope filter.

    Returns
    -------
    None
        Selectbox is displayed in the app where it is called.
    """
    df_areas = read_csv_file("areas.csv")
    st.selectbox(
        label="Geography",
        options=df_areas.drop("iso", axis=1).columns,
        index=0,
        key="geography",
        help="""Select the geography of interest. Only the texts that belong to NDCs in a selected
        geography will be returned. You can select a [Climate Promise](https://climatepromise.undp.org)
        group, geographic region or a specific country. Geographic regions are based on 
        [UNSD M49 Methodology](https://unstats.un.org/unsd/methodology/m49/).""",
    )


def add_version_select():
    """
    Add a select box for choosing an NDC version filter.

    Returns
    -------
    None
        Selectbox is displayed in the app where it is called.
    """
    options = st.session_state["versions"]
    version = st.selectbox(
        label="Version",
        options=options,
        index=0,
        key=None,
        help="""Select the version of interest. Only the texts that belong to NDCs of a selected
        version will be returned. Note that only the last available version of an NDC is stored for
        each country. Thus, you cannot use this filter to select past versions of the NDCs.
        **Selecting 'Version 1' will not return the first NDC version for all countries. Instead, it
        will return NDCs of those countries whose latest version is version 1.**""",
    )
    if version:
        st.session_state["version"] = options[version]


def add_category_select():
    """
    Add a select box for choosing a category filter.

    Returns
    -------
    None
        Selectbox is displayed in the app where it is called.
    """
    options = st.session_state["categories"]
    category = st.selectbox(
        label="Category",
        options=options,
        index=None,
        key=None,
        help="""Select the energy category of interest if applicable. Only the texts that are
        assigned a selected category will be returned. The number in the brackets indicates the
        total number of texts in a given category and does not take into account any filters you
        might have selected. You can leave this field empty.""",
        placeholder="Choose an option",
    )
    if category:
        st.session_state["category"] = options[category]


def add_date_slider():
    """
    Add a select box for choosing a search engine.

    Returns
    -------
    None
        Selectbox is displayed in the app where it is called.
    """
    date_range = st.session_state["date_range"]
    st.slider(
        label="Date Published",
        min_value=date_range[0],
        max_value=date_range[1],
        value=date_range,
        # step=1,
        key="dates",
        help="""Select a period of interest. Only the texts that belong to NDCs published within
        this period will be returned. Publication dates correspond to Submission Date in
        [NDC Registry](https://unfccc.int/NDCREG).""",
    )


def add_view_control() -> str:
    """
    Add a segmented control for view selection in search results.

    Returns
    -------
    None
        Segmented control is displayed in the app where it is called.
    """
    return st.segmented_control(
        label="View mode",
        options=["dropdown", "map"],
        selection_mode="single",
        default="dropdown",
        format_func=str.title,
        help="""Select a view mode to display detailed search results. Dropdown view allows you
        to select an NDC from a list view map view enables to explore NDC matches on a map.""",
    )


def add_ndc_select() -> str:
    """
    Add a select box for choosing a specific NDC from the list of matched results.

    Returns
    -------
    str
        Title of a selected NDC.
    """
    df = st.session_state["results"]
    return st.selectbox(
        label="NDC",
        options=df["title"].tolist(),
        index=0,
        help="""Select an NDC of interest to view relevant passages. NDCs in the dropdown are
        ordered by relevance (score) to your query. Matches within a given NDC are ordered by
        page. The score in brackets reflects the relevance of a match to your query. Higher
        scores reflect higher relevance.""",
        placeholder="Choose an NDC",
    )


def add_globe_toggle():
    """
    Add a toggle for switching between a map and globe view.

    Returns
    -------
    None
        Toggle is displayed in the app where it is called.
    """
    st.toggle(
        label="Display as a globe",
        value=False,
        key="globe",
        help="""By default, the map is shown using equirectangular projection. Turn on the
        toggle to display it as a globe using orthographic projection instead.""",
    )


def add_chat_input():
    """
    Add a chat input field for a user message.

    Returns
    -------
    None
        Chat input is displayed in the app where it is called.
    """
    placeholders = [
        "How to enhance the adaptive capacity of ecosystems to climate change?",
        "Give some examples of nature-based solutions.",
        "What is the base emission level in Zambia?",
        "Describe climate change adaptation measures in Egypt.",
        "Compare the climate change adaptation strategy of Pakistan with that of Egypt.",
    ]
    # only change the placeholder upon refresh to avoid state issues
    if not st.session_state.get("user_message"):
        st.session_state["placeholder"] = choice(placeholders)
    st.chat_input(
        placeholder=st.session_state["placeholder"],
        key="user_message",
        max_chars=256,
        disabled=False,
        on_submit=callbacks.retrieve,
    )
