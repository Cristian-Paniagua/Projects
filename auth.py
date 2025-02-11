import streamlit as st

def require_login():
    """
    Verifica si el usuario está logueado. Si no, redirige al login.
    """
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.warning("You must log in to access this page.")
        st.session_state["current_page"] = "login"
        st.stop()
