import streamlit as st
from core.style import inject_css
inject_css()
from core.qr_utils import decode_qr_from_bytes, verifier_certificat
from core.rag_engine import repondre_question
from core.logger import logger
from core.theme_utils import init_theme, theme_toggle
init_theme()
with st.sidebar:
    theme_toggle()
    st.markdown("---")   # séparateur
    if st.button("🚪 Se déconnecter"):
        # Supprimer l'utilisateur de la session
        del st.session_state.user
        # Rediriger vers la page de connexion
        st.switch_page("pages/0_Login.py")
# Vérification de l'authentification
if 'user' not in st.session_state:
    st.error("❌ Veuillez vous connecter pour accéder à cette page.")
    st.stop()

# Vérification du rôle (douane ou admin)
if st.session_state.user['role'] not in ['douane', 'admin']:
    st.error("🚫 Accès réservé aux agents de la douane et aux administrateurs.")
    st.stop()

st.markdown('<h1 class="main-header">🛃 Service Douane</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Vérifiez l’authenticité d’un certificat</p>', unsafe_allow_html=True)

st.markdown('<div class="card">', unsafe_allow_html=True)
uploaded_qr = st.file_uploader("📷 Scannez le QR Code (image)", type=["png", "jpg", "jpeg"])
if uploaded_qr is not None:
    st.image(uploaded_qr, caption="QR chargé", width=250)
    if st.button("✅ Vérifier le certificat", use_container_width=True):
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
                st.markdown('<div class="success-toast">✅ Certificat authentique ! Signature vérifiée.</div>', unsafe_allow_html=True)
                st.json(result["donnees"])
                if st.button("🔍 Obtenir les points de contrôle", use_container_width=True):
                    question = f"Quels sont les points de contrôle pour un lot de {result['donnees'].get('produit', 'produit')} grade {result['donnees'].get('grade', 'inconnu')} en provenance de {result['donnees'].get('origine', 'pays inconnu')} ?"
                    with st.spinner("Consultation de la base réglementaire..."):
                        reponse = repondre_question(question)
                    st.session_state.controle_reponse = reponse
                if "controle_reponse" in st.session_state:
                    st.markdown(f'<div class="card"><h3>📋 Points de contrôle</h3><p>{st.session_state.controle_reponse}</p></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="error-toast">❌ Signature invalide. Ce QR code a été falsifié.</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)