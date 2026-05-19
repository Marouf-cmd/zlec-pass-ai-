import streamlit as st
from core.style import inject_css
from core.theme_utils import theme_toggle
from core.config import PAYS_ZLECAF
from core.image_analyzer import analyze_product
from core.tariff_simulator import simuler_tarif
from core.qr_utils import generer_qr
from core.database import enregistrer_certification, get_commercant_info
from core.logger import logger
from PIL import Image
import tempfile
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

    st.markdown(f'<h1 class="main-header"><i class="fas fa-box"></i> {t("merchant_title")}</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="subtitle">Certifiez votre produit en quelques clics</p>', unsafe_allow_html=True)

    with st.sidebar:
        theme_toggle()
        st.markdown("---")
        language_selector()
        st.markdown("---")
        if st.button(t("logout_button")):
            del st.session_state.user
            st.switch_page("pages/0_Login.py")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    col_prod, col_info = st.columns([1, 2])
    with col_prod:
        produit_type = st.selectbox(t("product_type"), ["cafe", "cacao", "mais", "sorgho", "riz"])
    with col_info:
        nom_commercant = st.text_input(t("merchant_name"))
        if nom_commercant:
            info = get_commercant_info(nom_commercant)
            if info:
                st.markdown(f'<div style="padding: 0.5rem 1rem; margin-top: 0.5rem;">🏅 **{t("level")} :** {info["niveau"]} ({t("score")} {info["score"]})</div>', unsafe_allow_html=True)
            else:
                st.caption(t("new_merchant"))

    col_org, col_dest = st.columns(2)
    with col_org:
        origine = st.selectbox(t("origin"), PAYS_ZLECAF)
    with col_dest:
        destination = st.selectbox(t("destination"), PAYS_ZLECAF)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(f"📸 {t('upload_photo')}", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name

        col_img, col_btn = st.columns([2, 1])
        with col_img:
            image = Image.open(uploaded_file)
            st.image(image, caption="Aperçu", use_container_width=True)
        with col_btn:
            if st.button(f"🔍 {t('analyze_button')}", use_container_width=True):
                with st.spinner(t("loading")):
                    try:
                        resultat = analyze_product(tmp_path, product=produit_type)
                        if resultat:
                            st.session_state.analyse = resultat
                            st.session_state.simulation = None
                            st.session_state.qr_path = None
                            st.success(t("analysis_success"))
                        else:
                            st.error(t("analysis_failed"))
                    except Exception as e:
                        logger.error(f"Erreur analyse : {e}")
                        st.error(t("technical_error"))
    st.markdown('</div>', unsafe_allow_html=True)

    if "analyse" in st.session_state and st.session_state.analyse is not None:
        resultat = st.session_state.analyse
        produit = resultat["produit"]
        grade = resultat["grade"]

        if grade == "A":
            badge_html = f'<span class="badge-A">⭐ {t("grade_A")}</span>'
        elif grade == "B":
            badge_html = f'<span class="badge-B">📊 {t("grade_B")}</span>'
        else:
            badge_html = f'<span class="badge-C">⚠️ {t("grade_C")}</span>'

        st.markdown(f'<div class="card"><h3>📊 {t("analysis_result")}</h3><p><strong>{t("product")} :</strong> {produit}</p>{badge_html}</div>', unsafe_allow_html=True)

        if "simulation" not in st.session_state or st.session_state.simulation is None:
            st.session_state.simulation = simuler_tarif(produit, grade, origine, destination)
        simulation = st.session_state.simulation
        st.markdown(f'<div class="card"><h3>💰 {t("simulation")}</h3><p>{simulation}</p></div>', unsafe_allow_html=True)

        col_qr_btn, _ = st.columns([1, 3])
        with col_qr_btn:
            if st.button(f"📱 {t('generate_qr')}", use_container_width=True):
                donnees_cert = {
                    "commercant": nom_commercant,
                    "produit": produit,
                    "grade": grade,
                    "origine": origine,
                    "destination": destination,
                    "economie": simulation
                }
                chemin_qr = generer_qr(donnees_cert)
                st.session_state.qr_path = chemin_qr
                if nom_commercant:
                    enregistrer_certification(nom_commercant, produit, grade, origine, destination, simulation, "")
                    st.success(t("score_updated").format(name=nom_commercant))

        if "qr_path" in st.session_state and st.session_state.qr_path is not None:
            st.markdown('<div class="card qr-container">', unsafe_allow_html=True)
            st.image(st.session_state.qr_path, caption="QR Code de certification", width=250)
            with open(st.session_state.qr_path, "rb") as f:
                qr_data = f.read()
            st.download_button(f"⬇️ {t('download_qr')}", data=qr_data, file_name="certificat.png", mime="image/png")
            st.markdown('</div>', unsafe_allow_html=True)
except Exception as e:
    st.error(t("error_occurred"))
    logger.error(f"Erreur dans Commercant: {e}", exc_info=True)