import streamlit as st
from core.database import get_top_commercants, get_certifications
from core.logger import logger

st.header("Institution")

# Section : Classement des commerçants
st.subheader("🏆 Classement des commerçants (score de confiance)")
top_commercants = get_top_commercants(limit=10)
if top_commercants:
    for i, (nom, score) in enumerate(top_commercants, 1):
        st.write(f"{i}. **{nom}** – {score} points")
else:
    st.info("Aucun commerçant enregistré pour le moment.")

# Section : Liste des certifications
st.subheader("📋 Certifications enregistrées")
certifications = get_certifications()
if certifications:
    for cert in certifications:
        produit, grade, origine, destination, economie, horodatage, commerçant = cert
        with st.expander(f"{produit} – {commerçant} – {horodatage[:10]}"):
            st.write(f"**Grade:** {grade}")
            st.write(f"**Origine:** {origine}")
            st.write(f"**Destination:** {destination}")
            st.write(f"**Économie estimée:** {economie}")
            st.write(f"**Date/heure:** {horodatage}")
else:
    st.info("Aucune certification enregistrée pour le moment.")