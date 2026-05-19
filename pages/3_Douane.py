import streamlit as st
from core.style import inject_css
from core.theme_utils import theme_toggle
from core.qr_utils import decode_qr_from_bytes, verifier_certificat
from core.rag_engine import repondre_question
from core.logger import logger
from core.translations import t, language_selector, get_language

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

    if st.session_state.user['role'] not in ['douane', 'admin']:
        st.error("🚫 Accès réservé aux agents de la douane et aux administrateurs.")
        st.stop()

    with st.sidebar:
        theme_toggle()
        st.markdown("---")
        language_selector()
        st.markdown("---")
        if st.button(t("logout_button")):
            del st.session_state.user
            st.switch_page("pages/0_Login.py")

    st.markdown(f'<h1 class="main-header">🛃 {t("customs_title")}</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="subtitle">Vérifiez l’authenticité d’un certificat</p>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    uploaded_qr = st.file_uploader(f"📷 {t('scan_qr')}", type=["png", "jpg", "jpeg"])
    if uploaded_qr is not None:
        st.image(uploaded_qr, caption="QR chargé", width=250)
        if st.button(f"✅ {t('verify_button')}", use_container_width=True):
            try:
                image_bytes = uploaded_qr.getvalue()
                payload = decode_qr_from_bytes(image_bytes)
                valide, donnees = verifier_certificat(payload)
                st.session_state.verification_result = {
                    "valide": valide,
                    "donnees": donnees,
                    "payload": payload
                }
            except Exception as e:
                logger.error(f"Erreur vérification QR : {e}")
                st.session_state.verification_result = {"error": str(e)}

        if "verification_result" in st.session_state:
            result = st.session_state.verification_result
            if "error" in result:
                st.markdown(f'<div class="error-toast">❌ {result["error"]}</div>', unsafe_allow_html=True)
            else:
                if result["valide"]:
                    st.markdown(f'<div class="success-toast">✅ {t("certificate_valid")}</div>', unsafe_allow_html=True)
                    st.json(result["donnees"])
                    if st.button(f"🔍 {t('control_points_button')}", use_container_width=True):
                        question = f"Quels sont les points de contrôle pour un lot de {result['donnees'].get('produit', 'produit')} grade {result['donnees'].get('grade', 'inconnu')} en provenance de {result['donnees'].get('origine', 'pays inconnu')} ?"
                        with st.spinner(t("loading")):
                            reponse = repondre_question(question)
                        st.session_state.controle_reponse = reponse
                    if "controle_reponse" in st.session_state:
                        st.markdown(f'<div class="card"><h3>📋 {t("control_points")}</h3><p>{st.session_state.controle_reponse}</p></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="error-toast">❌ {t("certificate_invalid")}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
except Exception as e:
    st.error(t("error_occurred"))
    logger.error(f"Erreur dans Douane: {e}", exc_info=True)