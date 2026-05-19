import streamlit as st
from core.database import verify_user
from core.style import inject_css
from core.theme_utils import theme_toggle
from core.translations import t, language_selector, get_language
from core.logger import logger

try:
    inject_css()

    with st.sidebar:
        theme_toggle()
        st.markdown("---")
        language_selector()

    if 'user' in st.session_state:
        st.switch_page("pages/1_Accueil.py")

    if get_language() == "ar":
        st.markdown("""
        <style>
        .stApp { direction: rtl; }
        .stMarkdown, .stTextInput, .stSelectbox, .stButton { text-align: right; }
        </style>
        """, unsafe_allow_html=True)

    st.title(t("login_title"))
    username = st.text_input(t("username"))
    password = st.text_input(t("password"), type="password")

    if st.button(t("login_button")):
        user = verify_user(username, password)
        if user:
            st.session_state.user = user
            st.rerun()
        else:
            st.error(t("login_error"))
except Exception as e:
    st.error(t("error_occurred"))
    logger.error(f"Erreur dans Login: {e}", exc_info=True)