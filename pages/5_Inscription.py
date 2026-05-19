import streamlit as st
from core.style import inject_css
from core.theme_utils import theme_toggle
from core.database import add_user
from core.translations import t, language_selector, get_language
from core.logger import logger

try:
    inject_css()

    if get_language() == "ar":
        st.markdown("""
        <style>
        .stApp { direction: rtl; }
        .stMarkdown, .stTextInput, .stSelectbox, .stButton { text-align: right; }
        </style>
        """, unsafe_allow_html=True)

    with st.sidebar:
        theme_toggle()
        st.markdown("---")
        language_selector()
        st.markdown("---")
        st.markdown("💡 Déjà un compte ? [Se connecter](0_Login)")

    if 'user' in st.session_state:
        st.switch_page("pages/2_Commercant.py")

    st.title(t("register_title"))
    st.markdown(t("register_subtitle"))

    username = st.text_input(t("choose_username"))
    password = st.text_input(t("choose_password"), type="password")

    if st.button(t("create_account_button")):
        if username and password:
            if add_user(username, password, role='commercant'):
                st.success(t("account_created"))
                st.info(t("go_to_login"))
                if st.button(t("go_to_login")):
                    st.switch_page("pages/0_Login.py")
            else:
                st.error(t("username_exists"))
        else:
            st.error(t("fill_all_fields"))
except Exception as e:
    st.error(t("error_occurred"))
    logger.error(f"Erreur dans Inscription: {e}", exc_info=True)