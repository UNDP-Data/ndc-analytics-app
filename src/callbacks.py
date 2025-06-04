"""
Functions used as callbacks for input widgets.
"""

import numpy as np
import streamlit as st

from .database import search_documents
from .entities import Engine, Passage, Request
from .genai import embed_texts, paraphrase
from .utils import LANGUAGES


def search():
    """
    Run search using a request from the user and store the aggregated results in the session state.

    Returns
    -------
    None
        Stores the results in the session state under "results" key.
    """
    # create a search request from the session state
    request = Request(**st.session_state)
    if st.session_state["engine"] == Engine.NEURAL:
        request.query = embed_texts([request.query])[0]
    # run the search against NDC passages
    if (df := search_documents(request=request, limit=100)).empty:
        st.session_state["results"] = df
        return
    # remove redundant columns and calculate the score
    df.drop("vector", axis=1, inplace=True)
    if "_distance" in df.columns:
        df.eval("_score = (1 - _distance) * 100", inplace=True)
    df.rename({"_score": "score"}, axis=1, inplace=True)
    # recode langages for readability
    df["language"] = df["language"].map(LANGUAGES)
    # aggregate the results to NDC level
    df["matches"] = df[["pages", "text", "score"]].to_dict(orient="records")
    columns = [
        "file_name",
        "language",
        "iso",
        "party",
        "date",
        "version",
        "title",
        "type",
        "url",
    ]
    df = df.groupby(columns, as_index=False).agg({"matches": list})
    # add match count and score
    df["count"] = df["matches"].str.len()
    df["score"] = df["matches"].apply(
        lambda matches: np.quantile(
            [matches["score"] for matches in matches], q=0.75
        ).item()
    )
    df.sort_values("score", ascending=True, ignore_index=True, inplace=True)
    st.session_state["results"] = df


def retrieve():
    """
    Retrieve relevant passages using the request from the user and store
    the contexts in the session state.

    Returns
    -------
    None
        Stores the relevant contexts in the session state under "contexts" key.
    """
    st.session_state["query"] = paraphrase(
        st.session_state["user_message"], st.session_state["history"]
    )
    request = Request(engine=Engine.NEURAL, **st.session_state)
    request.query = embed_texts([request.query])[0]
    df = search_documents(request=request, limit=30)
    passages = [Passage(**doc).to_context() for doc in df.to_dict(orient="records")]
    st.session_state["contexts"] = passages
