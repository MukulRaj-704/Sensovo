# utils/state_utils.py
def init_session_state():
    import streamlit as st
    defaults = {
        'selected_movie': '',
        'selected_book': '',
        'page': 'Home'
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
