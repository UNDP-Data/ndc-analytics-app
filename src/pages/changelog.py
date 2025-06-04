"""
Streamlit page documenting releases.
"""

import st_undp
import streamlit as st

from src.utils import read_toml_file

col1, col2 = st.columns(2, gap="medium")
with col1:
    st_undp.featured_card(
        src="app/static/github-repository.jpg",
        title="ndc-analytics-app",
        summary="""This application is an open-source project under GNU AGPL-3.0 license.
        You can explore access its source code or open an issue on GitHub.""",
        href="https://github.com/UNDP-Data/ndc-analytics-app",
        tag="Source Code",
        width=12,
    )
with col2:
    changelog = read_toml_file("changelog.toml")
    for version, notes in changelog.items():
        with st.expander(f"Release v{version}", icon=":material/commit:"):
            st.markdown(notes)
