"""
Streamlit page for full-text search.
"""

import streamlit as st

from src import components

if st.session_state.get("results") is None:
    components.add_welcome_alert("search")
    st.stop()


tab1, tab2 = st.tabs(["Summary", "Details"])
if st.session_state["results"].empty:
    st.warning("No results found.")
    st.stop()
with tab1:
    components.add_results_metrics()
    components.add_results_dataframe()
with tab2:
    match components.add_view_control():
        case "dropdown":
            # dropdown items have a match count by definition
            title, count = components.add_ndc_select(), 1
        case "map":
            components.add_globe_toggle()
            title, count = components.add_plot_map()
            components.add_map_alert()
            if title is None:
                # no point is selected on the map
                st.warning("Select a party on the map to view matches.")
                st.stop()
            else:
                # display title only in the map view
                st.subheader(title)

    col1, col2 = st.columns(2)
    with col1:
        if count:
            components.add_text_expanders(title)
        else:
            st.warning("No matches.")
    with col2:
        components.add_source_button(title)
