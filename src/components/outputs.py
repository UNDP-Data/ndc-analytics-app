"""
Output elements fo building UI.
"""

import re
from random import choice

import st_undp
import streamlit as st
from annotated_text import annotated_text

from src.plotting import Colour, plot_map
from src.utils import complete_data_series, generate_ngrams, read_geojson

__all__ = [
    "add_results_metrics",
    "add_results_dataframe",
    "add_source_button",
    "add_text_expanders",
    "add_plot_map",
    "add_feed_expanders",
    "get_column_config",
]


def add_results_metrics():
    """
    Add stats cards containing search results metrics.

    Returns
    -------
    None
        Stats card is displayed in the app where it is called.
    """
    df = st.session_state["results"]
    col1, col2 = st.columns(2)
    with col1:
        st_undp.stats_card(
            value=len(df),
            title="NDCs Found",
            text="Total number of NDC documents that matched your filters",
        )

    with col2:
        st_undp.stats_card(
            value=df["count"].sum(),
            title="Passages Matched",
            text="Total number of passages in NDC documents that matched your filters",
        )


def get_column_config(max_count: int = 1, max_score: float = 1.0) -> dict:
    """
    Get a column config dictionary for prettifying the display of results data frame.

    Parameters
    ----------
    max_count : int, default=1
        The maximum value (scale) of the bar "#Passages" column.
    max_score : float, default=1.0
        The maximum value (scale) of the bar "Score" column.

    Returns
    -------
    dict
        Dictionary mapping column names to column configs to be used in `st.dataframe`.
    """
    config = {
        "Title": st.column_config.TextColumn(
            label="Title",
            width="medium",
        ),
        "Type": st.column_config.CheckboxColumn(
            label="Translation",
            width="small",
            help="Indicates if this document is a translation into English.",
            default=False,
        ),
        "Date": st.column_config.DatetimeColumn(
            label="Submission Date",
            # width="medium",
            help="Submission date",
            format="YYYY-MM-DD",
        ),
        "Url": st.column_config.LinkColumn(
            label="Source",
            width="small",
            help="The top trending Streamlit apps",
            display_text="Open link",
        ),
        "Count": st.column_config.ProgressColumn(
            label="#Passages",
            width="small",
            help="Number of passages matched in this document.",
            format="%d",
            min_value=0,
            max_value=max_count,
        ),
        "Score": st.column_config.ProgressColumn(
            label="Score",
            width="small",
            help="Full-text search score, with higher scores indicating higher relevance.",
            format="%.1f",
            min_value=0,
            max_value=max_score,
        ),
    }
    return config


def add_results_dataframe():
    """
    Display a data frame containing search results.

    Returns
    -------
    None
        Data frame is displayed in the app where it is called.
    """
    df = st.session_state["results"].copy()  # copy to avoid modifying the original
    df["type"] = df["type"].eq("translation")
    df["passage_example"] = df["matches"].apply(lambda matches: choice(matches)["text"])
    df.drop(["iso", "file_name", "matches"], axis=1, inplace=True)
    df.rename(lambda x: x.replace("_", " ").title(), axis=1, inplace=True)
    column_config = get_column_config(
        max_count=df["Count"].max().item(),
        max_score=df["Score"].max(),
    )
    st.dataframe(
        data=df,
        # height=len(df) * 20,
        use_container_width=True,
        hide_index=True,
        column_config=column_config,
    )


def add_source_button(title: str):
    """
    Add a link button to open a document source page.

    Returns
    -------
    None
        Link button is displayed in the app where it is called.
    """
    df = st.session_state["ndcs"]
    mapping = dict(df[["title", "url"]].values)
    st_undp.download_card(
        src=None,
        title=title,
        format="PDF",
        href=mapping[title],
        variant="default",
    )


def add_text_annotated(text: str, query: str):
    """
    Display annotated text using a naive implementation of text highlights.

    Parameters
    ----------
    text : str
        Input text to be displayed.
    query : str
        Query whose components will be highlighted in the text.

    Returns
    -------
    None
        Displays the annotated text.
    """
    annotations = []
    # strip special search syntax
    query = query.replace('"', "")
    ngrams = list(generate_ngrams(query))
    pattern = "|".join(ngrams)
    ngrams = set(ngrams)
    # keep the pattern after the split
    chunks = re.split(f"({pattern})", text, flags=re.IGNORECASE)
    for chunk in chunks:
        if chunk.strip().lower() in ngrams:
            annotations.append((chunk, "", Colour.YELLOW))
        else:
            annotations.append(chunk)
    annotated_text(*annotations)


def add_text_expanders(title: str):
    """
    Add text expanders for search results.

    Returns
    -------
    None
        Expanders are displayed in the app where the function is called.
    """
    df = st.session_state["results"]
    mapping = dict(df[["title", "matches"]].values)
    for match in mapping[title]:
        page = "-".join(str(page + 1) for page in match["pages"])
        title = f"Page {page} (score: {match['score']:.1f})"
        with st.expander(title):
            # st.info("Categories: " + (", ".join(match.categories) or "None"))
            add_text_annotated(match["text"], st.session_state["query"])


def add_plot_map() -> tuple[str | None, int | None]:
    """
    Add a map displaying search results.

    Returns
    -------
    None
        Map is displayed in the app where it is called.
    """
    df = complete_data_series(
        st.session_state["results"],
        st.session_state["ndcs"],
        read_geojson(),
    )
    projection = "orthographic" if st.session_state["globe"] else "equirectangular"
    fig = plot_map(df=df, projection=projection)
    selection = st.plotly_chart(
        figure_or_data=fig,
        use_container_width=True,
        theme=None,
        on_select="rerun",
        selection_mode="points",
    )
    if not (points := selection["selection"]["points"]):
        # no point is selected on the map
        return None, None
    point = points[0]
    return point["customdata"][1], point["z"]


def add_feed_expanders():
    """
    Add feed expanders for RSS items.

    Returns
    -------
    None
        Expanders are displayed in the app where the function is called.
    """
    feed = st.session_state["feed"]
    if not feed:
        st.error("Could not retrieve the feed. Please, try again later.")
    else:
        for item in feed:
            with st.expander(item.header):
                st.write(item.body)
