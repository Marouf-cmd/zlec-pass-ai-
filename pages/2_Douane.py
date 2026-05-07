import streamlit as st
from core.qr_utils import decode_qr_from_bytes, verifier_certificat
from core.rag_engine import repondre_question
from core.logger import logger

st.header("Douane")

uploaded_qr = st.file_uploader("Scanner le QR Code (image)", type=["png", "jpg", "jpeg"])
if uploaded_qr is not None:
    st.image(uploaded_qr, caption="QR du commerçant", width=400)
    
    if st.button("Vérifier le certificat"):
        try:
            # Utilisation directe des bytes de l'image
            image_bytes = uploaded_qr.getvalue()
            payload = decode_qr_from_bytes(image_bytes)
            valide, donnees = verifier_certificat(payload)
            st.session_state.verification_result = {
                "valide": valide,
                "donnees": donnees,
                "payload": payload
            }
        except Exception as e:
            logger.error(f"Échec vérification QR : {e}")
            st.session_state.verification_result = {"error": str(e)}
    
    # Affichage du résultat (identique à avant)
    if "verification_result" in st.session_state and st.session_state.verification_result is not None:
        result = st.session_state.verification_result
        if "error" in result:
            st.error(f"Impossible de décoder le QR code : {result['error']}")
        else:
            if result["valide"]:
                st.success("✅ Certificat authentique. Signature vérifiée.")
                st.json(result["donnees"])
                
                if st.button("Obtenir les points de contrôle"):
                    question = f"Quels sont les points de contrôle pour un lot de {result['donnees'].get('produit', 'produit')} grade {result['donnees'].get('grade', 'inconnu')} en provenance de {result['donnees'].get('origine', 'pays inconnu')} ?"
                    with st.spinner("Recherche en cours..."):
                        reponse = repondre_question(question)
                    st.session_state.controle_reponse = reponse
                
                if "controle_reponse" in st.session_state and st.session_state.controle_reponse is not None:
                    st.markdown(st.session_state.controle_reponse)
            else:
                st.error("❌ Signature invalide. Ce QR code a peut-être été falsifié.")