"""
Functions for interacting with LanceDB stored on Azure Blob Storage.
"""

import os

import duckdb
import lancedb
import pandas as pd
import streamlit as st

from .entities import Engine, Request
from .utils import LANGUAGES, read_csv_file

__all__ = ["get_connection", "get_table", "get_metadata", "search_documents"]


def get_connection() -> lancedb.DBConnection:
    """
    Get a database connection for LanceDB stored on Azure Blob Storage or locally.

    Returns
    -------
    lancedb.DBConnection
        Database connection client.
    """
    # if not connection details are present, use local storage
    if os.environ.get("STORAGE_ACCOUNT_NAME") is None:
        print("No Storage credentials are present. Connecting to a local LanceDB.")
        return lancedb.connect(os.path.join("data", "lancedb"))
    return lancedb.connect(
        "az://ndc-analytics-app/lancedb",
        storage_options={
            "account_name": os.environ["STORAGE_ACCOUNT_NAME"],
            "account_key": os.environ["STORAGE_ACCOUNT_KEY"],
        },
    )


def get_table() -> lancedb.table.Table:
    """
    Get a table object for NDCs from LanceDB.

    Returns
    -------
    lancedb.table.Table
        NDCs table object.
    """
    db = get_connection()
    table = db.open_table("ndcs")
    return table


@st.cache_resource(ttl="1h")
def get_metadata() -> dict:
    """
    Get metadata about NDC records from LanceDB.

    Returns
    -------
    dict
        Metadata about NDC records, including date range, categories,
        available version etc.
    """
    metadata = {}
    table = get_table()
    # accessible to DuckDB through the Arrow compatibility layer
    arrow_table = table.to_lance()

    # date range
    query = "SELECT min(date), max(date) FROM arrow_table"
    options = duckdb.query(query).fetchone()
    metadata["date_range"] = options

    # category options
    subquery = "SELECT UNNEST(categories) AS category FROM arrow_table"
    query = f"SELECT DISTINCT category, COUNT(*) AS count FROM ({subquery}) GROUP BY category"
    rows = duckdb.query(query).fetchall()
    options = {f"{category} ({count} items)": category for category, count in rows}
    metadata["categories"] = options

    # version options
    query = (
        "SELECT version, COUNT(DISTINCT iso) AS count FROM arrow_table GROUP BY version"
    )
    rows = duckdb.query(query).fetchall()
    options = {"All versions": None}
    options |= {f"Version {version} ({count} NDCs)": version for version, count in rows}
    metadata["versions"] = options

    # ndcs
    query = """
    SELECT DISTINCT url, iso, party, version, language, date, title, type
    FROM arrow_table
    ORDER BY date DESC
    """
    df = duckdb.query(query).to_df()
    df["language"] = df["language"].map(LANGUAGES)
    metadata["ndcs"] = df

    return metadata


def search_documents(request: Request, limit: int = 100) -> pd.DataFrame:
    """
    Run search in LanceDB against NDCs table.

    Depending on the request, this may be a full-text or vector search.

    Parameters
    ----------
    request : Request
        Search request.
    limit : int, default=100
        Maximum number of results to return.

    Returns
    -------
    pd.DataFrame
        Passages from NDCs table containing NDC metadata and passage text.
    """
    table = get_table()
    filters = [
        f"(date >= to_timestamp('{request.dates[0]}'))",
        f"(date <= to_timestamp('{request.dates[1]}'))",
    ]

    if request.engine != Engine.NEURAL:
        _, language = request.engine.name.split("_")
        filters.append(f"(language == '{language.lower()}')")

    if request.version is not None:
        filters.append(f"(version == {request.version})")

    if request.category:
        # filters.append(f"({request.category} in categories)")
        pass

    if request.geography:
        df_areas = read_csv_file("areas.csv")
        countries = df_areas.loc[df_areas[request.geography], "iso"].tolist()
        if len(countries) == 1:
            filters.append(f"(iso == '{countries[0]}')")
        elif request.geography != "All countries":
            filters.append(f"(iso in {tuple(countries)})")

    where = " AND ".join(filters)
    df = (
        table.search(request.query, query_type="auto", fts_columns="text")
        .where(where, prefilter=True)
        .limit(limit)
        # .select(["text", "date", "categories", "version"])
        .to_pandas()
    )
    return df
