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

inject_css()

if 'user' not in st.session_state:
    st.error("❌ Veuillez vous connecter pour accéder à cette page.")
    st.stop()

st.markdown('<h1 class="main-header"><i class="fas fa-box"></i> Espace Commerçant</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Certifiez votre produit en quelques clics</p>', unsafe_allow_html=True)

with st.sidebar:
    theme_toggle()
    st.markdown("---")
    if st.button("🚪 Se déconnecter"):
        del st.session_state.user
        st.switch_page("pages/0_Login.py")

# ... (reste du code inchangé)
# Section produit (carte)
st.markdown('<div class="card">', unsafe_allow_html=True)
col_prod, col_info = st.columns([1, 2])
with col_prod:
    produit_type = st.selectbox("🌾 Type de produit", ["cafe", "cacao", "mais", "sorgho", "riz"])
with col_info:
    nom_commercant = st.text_input("🏢 Nom du commerçant / exportateur")
    if nom_commercant:
        info = get_commercant_info(nom_commercant)
        if info:
            st.markdown(f'<div class="card" style="padding: 0.5rem 1rem; margin-top: 0.5rem;">🏅 **Niveau :** {info["niveau"]} (score {info["score"]})</div>', unsafe_allow_html=True)
        else:
            st.caption("🆕 Nouveau commerçant – débutera au niveau Bronze")

col_org, col_dest = st.columns(2)
with col_org:
    origine = st.selectbox("📍 Pays d'origine", PAYS_ZLECAF)
with col_dest:
    destination = st.selectbox("🎯 Pays de destination", PAYS_ZLECAF)
st.markdown('</div>', unsafe_allow_html=True)

# Upload de l'image
st.markdown('<div class="card">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("📸 Prenez une photo du produit", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name

    col_img, col_btn = st.columns([2, 1])
    with col_img:
        image = Image.open(uploaded_file)
        st.image(image, caption="Aperçu", use_container_width=True)
    with col_btn:
        if st.button("🔍 Analyser la qualité", use_container_width=True):
            with st.spinner("L'IA analyse l'image..."):
                try:
                    resultat = analyze_product(tmp_path, product=produit_type)
                    if resultat:
                        st.session_state.analyse = resultat
                        st.session_state.simulation = None
                        st.session_state.qr_path = None
                        st.success("✅ Analyse terminée !")
                    else:
                        st.error("❌ Échec de l'analyse. Réessayez.")
                except Exception as e:
                    logger.error(f"Erreur analyse : {e}")
                    st.error("Une erreur technique s'est produite.")
st.markdown('</div>', unsafe_allow_html=True)

# Résultats et simulation
if "analyse" in st.session_state and st.session_state.analyse is not None:
    resultat = st.session_state.analyse
    produit = resultat["produit"]
    grade = resultat["grade"]

    if grade == "A":
        badge_html = '<span class="badge-A">⭐ Grade A - Haute qualité</span>'
    elif grade == "B":
        badge_html = '<span class="badge-B">📊 Grade B - Qualité moyenne</span>'
    else:
        badge_html = '<span class="badge-C">⚠️ Grade C - Qualité inférieure</span>'

    st.markdown(f'<div class="card"><h3>📊 Résultat de l’analyse</h3><p><strong>Produit :</strong> {produit}</p>{badge_html}</div>', unsafe_allow_html=True)

    # Simulation tarifaire
    if "simulation" not in st.session_state or st.session_state.simulation is None:
        st.session_state.simulation = simuler_tarif(produit, grade, origine, destination)
    simulation = st.session_state.simulation
    st.markdown(f'<div class="card"><h3>💰 Simulation douanière</h3><p>{simulation}</p></div>', unsafe_allow_html=True)

    # Génération du QR Code
    col_qr_btn, _ = st.columns([1, 3])
    with col_qr_btn:
        if st.button("📱 Générer le QR Code", use_container_width=True):
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
                st.success(f"🏅 Score de confiance mis à jour pour {nom_commercant}")

    # Affichage et téléchargement du QR
    if "qr_path" in st.session_state and st.session_state.qr_path is not None:
        st.markdown('<div class="card qr-container">', unsafe_allow_html=True)
        st.image(st.session_state.qr_path, caption="QR Code de certification", width=250)
        with open(st.session_state.qr_path, "rb") as f:
            qr_data = f.read()
        st.download_button("⬇️ Télécharger le QR", data=qr_data, file_name="certificat.png", mime="image/png")
        st.markdown('</div>', unsafe_allow_html=True)