import streamlit as st
from core.database import verify_user

# Si l'utilisateur est déjà connecté, on le redirige vers la page commerçant
if 'user' in st.session_state:
    st.switch_page("pages/1_Accueil.py")

st.title("Connexion")

# Formulaire de connexion
username = st.text_input("Nom d'utilisateur")
password = st.text_input("Mot de passe", type="password")

if st.button("Se connecter"):
    user = verify_user(username, password)
    if user:
        st.session_state.user = user   # Stocke l'utilisateur dans la session
        st.rerun()                      # Recharge l'application (redirige vers la page commerçant)
    else:
        st.error("Échec de la connexion. Vérifiez vos identifiants.")