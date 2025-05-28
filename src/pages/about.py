"""
Streamlit page for about information.
"""

import streamlit as st

from src import utils

body = utils.read_text_file("about.md")
st.markdown(body)
