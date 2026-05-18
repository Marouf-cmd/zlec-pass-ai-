import streamlit as st
from core.database import init_db
init_db()
st.set_page_config(page_title="ZLEC-Pass AI", page_icon="🌍", layout="wide")
st.title("Bienvenue sur ZLEC-Pass AI")
st.write("Utilisez la barre latérale pour naviguer.")
