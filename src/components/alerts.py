"""
Info, warnings and error elements fo creating alerts.
"""

from typing import Literal

import streamlit as st

__all__ = [
    "add_welcome_alert",
    "add_noresults_alert",
    "add_rss_alert",
    "add_ndcs_alert",
    "add_map_alert",
]


def add_welcome_alert(page: Literal["search", "ask"]):
    """
    Add a welcome alert to search or ask pages.

    Parameters
    ----------
    page : Literal["search", "ask"]
        The page to the alert is indended to be used on.

    Returns
    -------
    None
        Alert is displayed in the app where it is called.
    """
    if page == "search":
        message = (
            "Configure the filters in the sidebar on the left to "
            "search more than 30k paragraphs from over 100 NDCs. "
            "See the [query guide](./about#query-guide) to understand how this search works."
        )
    elif page == "ask":
        message = (
            "Enter your message below to ask an AI model to provide "
            "a response based on more than 30k paragraphs from over 100 NDCs. "
            "This feature is powered by Azure OpenAI Service (GPT-4o mini). "
            "For cutting-edge GenAI capabilities, visit "
            "[DFx AI Chat](https://chat.data.undp.org?utm_source=ndc-analytics-app)."
        )
    else:
        raise ValueError("page not recognised")
    st.info(message, icon=":material/lightbulb:")


def add_noresults_alert():
    """
    Add an alert when no results are found.

    Returns
    -------
    None
        Alert is displayed in the app where it is called.
    """
    message = (
        "Sorry, we could not find anything relevant for your search options. "
        "Remove some of the filters or use a different query, then try searching again."
    )
    st.warning(message, icon=":material/info:")


def add_rss_alert():
    """
    Add an alert about RSS page.

    Returns
    -------
    None
        Alert is displayed in the app where it is called.
    """
    message = (
        "This page shows the latest items from the RSS Feed of "
        "[NDC Registry](https://unfccc.int/NDCREG). "
        "You can use it to stay up to date with the latest submissions and updates in the registry."
    )
    st.info(message, icon=":material/lightbulb:")


def add_ndcs_alert():
    """
    Add an alert about NDCs page.

    Returns
    -------
    None
        Alert is displayed in the app where it is called.
    """
    message = (
        "The information on this page refers to the NDCs included in the database"
        " that is used by this application. "
        "It may not fully align with data on [NDC Registry](https://unfccc.int/NDCREG). "
        "See [About](./about) for more details."
    )
    st.info(message, icon=":material/lightbulb:")


def add_map_alert():
    """
    Add an alert about geographic entities on the map.

    Returns
    -------
    None
        Alert is displayed in the app where it is called.
    """
    message = (
        "The map is shown for illustration purposes only."
        " The boundaries and names shown and the designations used on this map do not"
        " imply official endorsement or acceptance by the United Nations."
    )
    st.info(message, icon=":material/warning:")
