"""
Streamlit page for displaying NDCs from the database.
"""

import st_undp
import streamlit as st

from src.components import add_ndcs_alert, get_column_config

df_ndcs = st.session_state["ndcs"].copy()  # make a copy not to modify the original

col1, col2, col3 = st.columns(3)
with col1:
    st_undp.stats_card(
        value=df_ndcs["party"].nunique(),
        title="Parties",
        text="Total number of parties (countries) that submitted NDCs",
    )

with col2:
    st_undp.stats_card(
        value=df_ndcs.shape[0],
        title="NDCs",
        text="Total number of NDCs in the database, including original and translated ones",
    )

with col3:
    st_undp.stats_card(
        value=f"{df_ndcs.date.min():%Y}-{df_ndcs.date.max():%Y}",
        title="Period",
        text=f"""Covers the NDCs submitted between {df_ndcs.date.min():%B %Y}
         and {df_ndcs.date.max():%B %Y}""",
    )

df_ndcs["type"] = df_ndcs["type"].eq("translation")
df_ndcs.drop(columns=["iso"], inplace=True)
df_ndcs.rename(lambda x: x.title(), axis=1, inplace=True)

add_ndcs_alert()

st.dataframe(
    data=df_ndcs,
    height=600,
    use_container_width=True,
    hide_index=True,
    column_config=get_column_config(),
)
