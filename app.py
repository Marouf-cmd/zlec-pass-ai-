import streamlit as st
import config
import database
from translations import translations as tr
import os
from image_analyzer import analyze_product
from tariff_simulator import simuler_tarif
from qr_utils import generer_qr
import database
from PIL import Image
import tempfile


# Initialiser la base de données
database.init_db()

# Config de page
st.set_page_config(page_title="ZLEC-Pass AI", layout="wide")

# Langue (par défaut français)
lang = st.sidebar.selectbox("Langue / اللغة", ["Français", "العربية"])
if lang == "العربية":
    lang_key = "ar"
else:
    lang_key = "fr"
t = tr[lang_key]

st.title(t["title"])

# Menu de mode
mode = st.sidebar.radio("Mode", [
    t.get("trader_mode", "Commerçant"),
    t.get("customs_mode", "Douane"),
    t.get("institution_mode", "Institution")
])
if mode == t.get("trader_mode", "Commerçant"):
    st.header(t.get("trader_mode", "Commerçant"))
    
    nom_commercant = st.text_input("Nom du commerçant / exportateur")
    origine = st.selectbox(t.get("origin", "Pays d'origine"), config.PAYS_ZLECAF)
    destination = st.selectbox(t.get("destination", "Pays de destination"), config.PAYS_ZLECAF)
    
    uploaded_file = st.file_uploader("Photo du produit", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        # Sauvegarde temporaire
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name
        
        image = Image.open(uploaded_file)
        st.image(image, caption="Produit photographié", use_container_width=True)
        
        # Bouton d'analyse – indépendant, ne contient pas le QR bouton
        if st.button(t.get("analyze", "Analyser la qualité")):
            with st.spinner("Analyse IA en cours..."):
                resultat = analyze_product(tmp_path)
                if resultat:
                    st.session_state.analyse = resultat
                    # On efface l'ancienne simulation et QR pour éviter les mélanges
                    st.session_state.simulation = None
                    st.session_state.qr_path = None
                else:
                    st.error("Échec de l'analyse. Réessayez.")
        
        # Si une analyse existe, on affiche ses résultats et on propose la simulation + QR
        if "analyse" in st.session_state and st.session_state.analyse is not None:
            resultat = st.session_state.analyse
            produit = resultat["produit"]
            grade = resultat["grade"]
            st.success(f"Produit : {produit} | Grade : {grade}")
            
            # Simulation (on ne la calcule qu'une fois si elle n'existe pas déjà)
            if "simulation" not in st.session_state or st.session_state.simulation is None:
                st.session_state.simulation = simuler_tarif(produit, grade, origine, destination)
            simulation = st.session_state.simulation
            st.info(simulation)
            
            # Bouton pour générer le QR code – complètement indépendant
            if st.button(t.get("generate_qr", "Générer le QR Code")):
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
                    database.enregistrer_certification(
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
elif mode == t.get("customs_mode", "Douane"):
    st.header(t.get("customs_mode", "Douane"))
    st.write("Interface douane en construction...")
else:
    st.header(t.get("institution_mode", "Institution"))
    st.write("Tableau de bord en construction...")
