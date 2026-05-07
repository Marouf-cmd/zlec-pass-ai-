import streamlit as st
from core.config import PAYS_ZLECAF
from core.image_analyzer import analyze_product
from core.tariff_simulator import simuler_tarif
from core.qr_utils import generer_qr
from core.database import enregistrer_certification
from core.logger import logger
from PIL import Image
import tempfile

st.header("Commerçant")
    
nom_commercant = st.text_input("Nom du commerçant / exportateur")
origine = st.selectbox("Pays d'origine", PAYS_ZLECAF)
destination = st.selectbox("Pays de destination", PAYS_ZLECAF)
    
uploaded_file = st.file_uploader("Photo du produit", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    # Sauvegarde temporaire
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name
    
    image = Image.open(uploaded_file)
    st.image(image, caption="Produit photographié", use_container_width=True)
    
    # Bouton d'analyse
    if st.button("Analyser la qualité"):
        with st.spinner("Analyse IA en cours..."):
            try:
                resultat = analyze_product(tmp_path)
                if resultat:
                    st.session_state.analyse = resultat
                    st.session_state.simulation = None
                    st.session_state.qr_path = None
                else:
                    st.error("Échec de l'analyse. Réessayez.")
            except Exception as e:
                logger.error(f"Erreur analyse produit : {e}")
                st.error("Une erreur est survenue pendant l'analyse. Veuillez réessayer.")
    
    # Si une analyse existe, on affiche ses résultats et on propose la simulation + QR
    if "analyse" in st.session_state and st.session_state.analyse is not None:
        resultat = st.session_state.analyse
        produit = resultat["produit"]
        grade = resultat["grade"]
        st.success(f"Produit : {produit} | Grade : {grade}")
        
        # Simulation (une seule fois)
        if "simulation" not in st.session_state or st.session_state.simulation is None:
            st.session_state.simulation = simuler_tarif(produit, grade, origine, destination)
        simulation = st.session_state.simulation
        st.info(simulation)
        
        # Bouton pour générer le QR code
        if st.button("Générer le QR Code"):
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
            # Enregistrer en base
            if nom_commercant:
                enregistrer_certification(
                    nom_commercant, produit, grade, origine, destination,
                    simulation, ""  # signature pas stockée
                )
                st.success(f"Score de confiance de {nom_commercant} mis à jour.")
        
        # Affichage du QR code s'il a été généré
        if "qr_path" in st.session_state and st.session_state.qr_path is not None:
            st.image(st.session_state.qr_path, caption="QR Code de certification", width=300)
            with open(st.session_state.qr_path, "rb") as f:
                qr_data = f.read()
            st.download_button("Télécharger le QR Code", data=qr_data, file_name="certificat.png", mime="image/png")