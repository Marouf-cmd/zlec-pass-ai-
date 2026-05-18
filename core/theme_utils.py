import streamlit as st

def theme_toggle():
    current = st.query_params.get("theme", "light")
    label = "🌙 Thème sombre" if current == "light" else "☀️ Thème clair"
    if st.button(label):
        new_theme = "dark" if current == "light" else "light"
        st.query_params["theme"] = new_theme
        st.rerun()