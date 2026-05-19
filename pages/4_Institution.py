import streamlit as st
from core.style import inject_css
from core.theme_utils import theme_toggle
from core.database import get_top_commercants, get_certifications
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

    if 'user' not in st.session_state:
        st.error(t("login_error"))
        st.stop()

    if st.session_state.user['role'] not in ['admin', 'institution']:
        st.error("🚫 Accès réservé aux administrateurs et aux institutionnels.")
        st.stop()

    with st.sidebar:
        theme_toggle()
        st.markdown("---")
        language_selector()
        st.markdown("---")
        if st.button(t("logout_button")):
            del st.session_state.user
            st.switch_page("pages/0_Login.py")

    st.markdown(f'<h1 class="main-header">🏛️ {t("institution_title")}</h1>', unsafe_allow_html=True)

    # Métriques (exemples)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="metric-card"><div class="metric-value">15</div><div class="metric-label">Commerçants actifs</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><div class="metric-value">48</div><div class="metric-label">Certifications</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><div class="metric-value">12</div><div class="metric-label">Pays couverts</div></div>', unsafe_allow_html=True)

    # Classement
    st.markdown(f'<div class="card"><h3>🏆 {t("top_merchants")}</h3>', unsafe_allow_html=True)
    top_commercants = get_top_commercants(limit=10)
    if top_commercants:
        table_html = f'<table class="data-table"><thead><tr><th>{t("rank")}</th><th>{t("name")}</th><th>{t("score")}</th><th>{t("level")}</th></tr></thead><tbody>'
        for i, (nom, score, niveau) in enumerate(top_commercants, 1):
            table_html += f'<tr><td>{i}</td><td>{nom}</td><td>{score}</td><td>{niveau}</td></tr>'
        table_html += '</tbody></table>'
        st.markdown(table_html, unsafe_allow_html=True)
    else:
        st.info(t("no_merchants"))
    st.markdown('</div>', unsafe_allow_html=True)

    # Certifications récentes
    st.markdown(f'<div class="card"><h3>📜 {t("recent_certifications")}</h3>', unsafe_allow_html=True)
    certifications = get_certifications()
    if certifications:
        for cert in certifications[:5]:
            produit, grade, origine, destination, economie, horodatage, commerçant = cert
            if grade == "A":
                grade_badge = '<span class="badge-A">A</span>'
            elif grade == "B":
                grade_badge = '<span class="badge-B">B</span>'
            else:
                grade_badge = '<span class="badge-C">C</span>'
            st.markdown(f"""
            <div style="border-bottom:1px solid #eee; padding:0.5rem 0;">
                <strong>{commerçant}</strong> – {produit} {grade_badge}<br>
                <small>Origine : {origine} | Destination : {destination} | Le {horodatage[:10]}</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info(t("no_certifications"))
    st.markdown('</div>', unsafe_allow_html=True)
except Exception as e:
    st.error(t("error_occurred"))
    logger.error(f"Erreur dans Institution: {e}", exc_info=True)