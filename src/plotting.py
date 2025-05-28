"""
Functions for plotting graphs.
"""

from enum import StrEnum

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from .utils import read_geojson

__all__ = ["BLUES", "GRAYS", "Colour", "plot_map"]

BLUES = ["#B5D5F5", "#94C4F5", "#6BABEB", "#4F95DD", "#3288CE", "#006EB5", "#1F5A95"]
GRAYS = ["#FAFAFA", "#F7F7F7", "#EDEFF0", "#D4D6D8", "#A9B1B7", "#55606E", "#232E3D"]


class Colour(StrEnum):
    """
    Colours as per the UNDP Design System.
    See https://design.undp.org/?path=/docs/foundation-colors--docs.
    """

    # accent colours
    LIGHT_YELLOW = "#FFEB00"
    YELLOW = "#FFEB00"
    DARK_YELLOW = "#FBC412"
    LIGHT_RED = "#FFBCB7"
    RED = "#EE402D"
    DARK_RED = "#D12800"
    LIGHT_GREEN = "#B8ECB6"
    GREEN = "#6DE354"
    DARK_GREEN = "#59BA47"
    LIGHT_AZURE = "#A2DAF3"
    AZURE = "#60D4F2"
    DARK_AZURE = "#00C1FF"
    # aliases
    PRIMARY = "#006EB5"  # blue-600


def __format_tooltip(row: pd.Series) -> str:
    """
    Format a tooltip for displaying search results data on a map.
    """
    title = f"<b>{row.party}</b><br>"
    # not NDC published
    if (count := row["count"]) == -1:
        return title + "No NDC available."
    return (
        f"{title}Version: {row.version:.0f}<br>"
        f"Submission Date: {row.date: %B %d, %Y}<br>"
        f"Number of matches: {count:.0f}<br>"
    )


def plot_map(df: pd.DataFrame, projection: str) -> go.Figure:
    """
    Plot a choropleth map of NDC matches.

    Parameters
    ----------
    df : pd.DataFrame
        Data frame containing NDC matches data.
    projection : str
        Type of projection to use.

    Returns
    -------
    go.Figure
        Choropleth with a time slider.
    """
    # sort to avoid issues with the tooltip
    df = df.sort_values(["date", "iso"], ignore_index=True)
    df["tooltip"] = df.apply(__format_tooltip, axis=1)

    geojson = read_geojson()
    fig = px.choropleth(
        data_frame=df,
        locations="iso",
        geojson=geojson,
        featureidkey="properties.iso3cd",
        color="count",
        custom_data=["tooltip", "title"],  # include the title for matching the section
        color_continuous_scale=[GRAYS[0], GRAYS[3]] + BLUES,
        animation_frame="year",
        projection=projection,
        range_color=[df["count"].min(), df["count"].max()],
        basemap_visible=False,
        title="Search Results for NDC Parties",
        height=600,
    )
    for frame in fig.frames:
        for trace in frame.data:
            trace.update(hovertemplate="%{customdata[0]}")
    fig.update_layout(
        autosize=True,
        margin={
            "l": 0,
            "r": 0,
            "b": 0,
            # "t": 0,
            "pad": 0,
            "autoexpand": True,
        },
        geo={"showframe": False},
        coloraxis_colorbar={"title": "#Passages"},
        sliders=[{"currentvalue": {"prefix": "Year: "}}],
    )
    return fig
