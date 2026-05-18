import streamlit as st
from core.database import verify_user
from core.style import inject_css
from core.theme_utils import theme_toggle

# Injecter les styles (cela inclut le script de thème)
inject_css()

# Barre latérale avec bouton de changement de thème
with st.sidebar:
    theme_toggle()

# Redirection si déjà connecté
if 'user' in st.session_state:
    st.switch_page("pages/1_Accueil.py")

st.title("Connexion")

username = st.text_input("Nom d'utilisateur")
password = st.text_input("Mot de passe", type="password")

if st.button("Se connecter"):
    user = verify_user(username, password)
    if user:
        st.session_state.user = user
        st.rerun()
    else:
        st.error("Échec de la connexion. Vérifiez vos identifiants.")