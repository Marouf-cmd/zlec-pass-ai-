import streamlit as st
import config
import database
from translations import translations as tr
import os

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
    st.write("Interface commerçant en construction...")
elif mode == t.get("customs_mode", "Douane"):
    st.header(t.get("customs_mode", "Douane"))
    st.write("Interface douane en construction...")
else:
    st.header(t.get("institution_mode", "Institution"))
    st.write("Tableau de bord en construction...")
