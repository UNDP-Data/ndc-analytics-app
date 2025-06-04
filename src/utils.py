"""
Miscellaneous utility function for reading and parsing data.
"""

import json
import re
import tomllib
import xml.etree.ElementTree as ET
from importlib import resources

import pandas as pd
import requests

from .entities import FeedItem

__all__ = [
    "read_text_file",
    "read_csv_file",
    "read_geojson",
    "read_toml_file",
    "read_prompts",
    "get_feed",
    "generate_ngrams",
    "complete_data_series",
]


def read_text_file(file_name: str) -> str:
    """
    Read a text file from the package's `data` directory.

    Parameters
    ----------
    file_name : str
        Name of the file to read.

    Returns
    -------
    str
        Content of the file as a string.
    """
    with resources.open_text("src.data", file_name) as file:
        return file.read()


def read_csv_file(file_name: str) -> pd.DataFrame:
    """
    Read a CSV file from the package's `data` directory.

    Parameters
    ----------
    file_name : str
        Name of the file to read.

    Returns
    -------
    pd.DataFrame
        Content of the file as a data frame.
    """
    with resources.open_text("src.data", file_name) as file:
        return pd.read_csv(file)


def read_geojson() -> dict:
    """
    Read a GeoJSON of country polygons from the United Nations Secretariat.

    The file can be downloaded from
    https://geoportal.un.org/arcgis/home/item.html?id=d7caaff3ef4b4f7c82689b7c4694ad92
    (newer versions might exist). The file does not work with Plotly out of the box and
    requires transformation into gj2008 specification. See
    https://github.com/mbloch/mapshaper/issues/432#issuecomment-675775465 for more details.

    Returns
    -------
    dict
        GeoJSON of the country polygons.
    """
    with resources.open_text("src.data", "countries.geojson") as file:
        return json.load(file)


def read_toml_file(file_name: str) -> dict:
    """
    Read a TOML file from the package's `data` directory.

    Parameters
    ----------
    file_name : str
        Name of the file to read.

    Returns
    -------
    dict
        Contents of the TOML file as a dictionary.
    """
    text = read_text_file(file_name)
    return tomllib.loads(text)


def read_prompts() -> dict:
    """
    Read the prompts from the package's `data` directory.

    Returns
    -------
    dict
        Dictionary mapping names to prompts.
    """
    return read_toml_file("promps.toml")


def get_feed() -> list[FeedItem]:
    """
    Get the RSS feed from NDC Registry.

    Returns
    -------
    list[FeedItem]
        List of RSS feed items.
    """
    try:
        response = requests.get(
            url="https://unfccc.int/NDCREG/rss.xml",
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10,
        )
        response.raise_for_status()
    except requests.RequestException:
        return []
    root = ET.fromstring(response.text)
    namespaces = {"dc": "http://purl.org/dc/elements/1.1/"}
    return [FeedItem.from_xml(item, namespaces) for item in root.findall(".//item")]


def generate_ngrams(
    text: str,
    min_size: int = 1,
    max_size: int = 5,
) -> list[str]:
    """
    Generate n-grams from an abitrary text.

    This function is used to heuristically highlight parts of retrieved passages
    relevant to a user query.

    Parameters
    ----------
    text : str
        Input text.
    min_size : int, default=1
        Minimum length of an n-gram.
    max_size : int, default=5
        Maximum length of an n-gram.

    Returns
    -------
    ngrams : list[str]
        List of n-grams from the longest to the shortest.

    Examples
    --------
    >>> from pprint import pprint
    >>> text = "Colorless green ideas sleep furiously"
    >>> pprint(generate_ngrams(text))
    ['Colorless green ideas sleep furiously',
     'Colorless green ideas sleep',
     'green ideas sleep furiously',
     'Colorless green ideas',
     'green ideas sleep',
     'ideas sleep furiously',
     'Colorless green',
     'green ideas',
     'ideas sleep',
     'sleep furiously',
     'Colorless',
     'green',
     'ideas',
     'sleep',
     'furiously']
    """
    assert min_size <= max_size, "min_size must be less than max_size"
    tokens = text.split()
    # from the longest to shortest
    sizes = sorted(range(1, max_size + 1), reverse=True)
    ngrams = []
    stopwords = {
        word.strip() for word in read_text_file("stopwords.txt").split() if word.strip()
    }
    pattern = "|".join(stopwords)
    for size in sizes:
        for i in range(len(tokens) - size + 1):
            ngram = " ".join(tokens[i : i + size])
            # remove stopwords and ngrams starting with a stopword
            if ngram in stopwords:
                continue
            if re.match(f"{pattern}\b", ngram, flags=re.IGNORECASE):
                continue
            ngrams.append(ngram)
    return ngrams


def complete_data_series(
    df_results: pd.DataFrame, df_ndcs: pd.DataFrame, geojson: dict
) -> pd.DataFrame:
    """
    Complete search results to have a full panel dataset for visualisation.

    The function takes search results, a full list of NDCs and a geojson containing
    country geometrues to create a cartesian product of all country-years. In the full
    dataset the country-year pairs that have an NDC published but no matches are
    distinguished from those that have no NDC in the first place.

    Parameters
    ----------
    df_results : pd.DataFrame
        Data frame of search results, assigned to the session state
        by a `search` callback.
    df_ndcs : pd.DataFrame
        Data frame of NDCs in the database, assigned the the session state
        by `get_metadata`.
    geojson : dict
        Geojson containing country geometries as returned by `read_geojson`.

    Returns
    -------
    pd.DataFrame
        Complete panel dataset containing observations for all countries in
        all years. `count` column contains a positibe number for NDCs that
        have a match, `0` for those that don't and `-1` for those that do
        not have a published NDC in that year.
    """
    # keep the highest match count for results (of both original and translation are present)
    df_results["year"] = df_results["date"].dt.year
    df_results = (
        df_results.sort_values("count", ascending=False)
        .groupby(["iso", "date"])
        .head(1)
    )

    # get basic country metadata from GeoJSON
    df_countries = pd.DataFrame(
        [feature["properties"] for feature in geojson["features"]]
    )
    df_countries.rename(columns={"iso3cd": "iso", "nam_en": "party"}, inplace=True)

    # create a panel dataset (country-year panes)
    df_panel = pd.merge(
        df_countries,
        df_results["year"].drop_duplicates(ignore_index=True).astype(int),
        how="cross",
    )

    # add metadata for all NDCs
    df_ndcs["year"] = pd.to_datetime(df_ndcs["date"]).dt.year
    df_panel = df_panel.merge(
        df_ndcs[["iso", "year", "title", "version", "date"]].drop_duplicates(),
        how="left",
        on=["iso", "year"],
        indicator=True,
    )

    # add the count of result matches
    df_panel = df_panel.merge(
        df_results[["iso", "year", "count"]],
        how="left",
        on=["iso", "year"],
    )

    # there is no NDC for a country in that year
    df_panel.loc[df_panel["_merge"].eq("left_only"), "count"] = -1.0

    # otherwise, there is no match for an existing NDC
    df_panel.fillna({"count": 0.0}, inplace=True)
    return df_panel
