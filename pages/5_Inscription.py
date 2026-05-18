import streamlit as st
from core.database import add_user

# Si déjà connecté, rediriger vers la page commerçant
if 'user' in st.session_state:
    st.switch_page("pages/2_Commercant.py")

st.title("📝 Inscription Commerçant")
st.markdown("Créez votre compte pour accéder à l'espace de certification.")

username = st.text_input("👤 Choisissez un identifiant")
password = st.text_input("🔒 Mot de passe", type="password")

if st.button("Créer mon compte"):
    if username and password:
        if add_user(username, password, role='commercant'):
            st.success("✅ Compte créé avec succès ! Vous pouvez maintenant vous connecter.")
            st.info("🔐 Allez sur la page **Connexion** pour vous identifier.")
        else:
            st.error("Ce nom d'utilisateur existe déjà.")
    else:
        st.error("Veuillez remplir tous les champs.")