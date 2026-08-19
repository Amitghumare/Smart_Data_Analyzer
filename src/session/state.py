import streamlit as st


def initialize_session_state():
    """
    Initialize all session-state variables used
    throughout the Smart Data Analyzer application.
    """

    defaults = {
        "dataset": None,
        "cleaned_data": None,
        "file_name": None,
        "dataset_loaded": False,
        "cleaning_applied": False,
        "current_page": "upload",
        "visualizations": [],
        "insights": [],
        "report_generated": False,
    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value