import streamlit as st
from core.style import inject_css
inject_css()
from core.database import get_top_commercants, get_certifications
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

st.markdown('<h1 class="main-header">🏛️ Tableau de bord institutionnel</h1>', unsafe_allow_html=True)


# Métriques (exemple factice, à adapter avec vos propres compteurs)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="metric-card"><div class="metric-value">15</div><div class="metric-label">Commerçants actifs</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-card"><div class="metric-value">48</div><div class="metric-label">Certifications</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-card"><div class="metric-value">12</div><div class="metric-label">Pays couverts</div></div>', unsafe_allow_html=True)

# Classement
st.markdown('<div class="card"><h3>🏆 Top 10 des commerçants (score de confiance)</h3>', unsafe_allow_html=True)
top_commercants = get_top_commercants(limit=10)
if top_commercants:
    table_html = '<table class="data-table"><thead><tr><th>Rang</th><th>Nom</th><th>Score</th></tr></thead><tbody>'
    for i, (nom, score) in enumerate(top_commercants, 1):
        table_html += f'<tr><td>{i}</td><td>{nom}</td><td>{score}</td></tr>'
    table_html += '</tbody></table>'
    st.markdown(table_html, unsafe_allow_html=True)
else:
    st.info("Aucun commerçant enregistré pour le moment.")
st.markdown('</div>', unsafe_allow_html=True)

# Certifications récentes
st.markdown('<div class="card"><h3>📜 Dernières certifications</h3>', unsafe_allow_html=True)
certifications = get_certifications()
if certifications:
    for cert in certifications[:5]:  # seulement les 5 dernières
        produit, grade, origine, destination, economie, horodatage, commerçant = cert
        # Badge de grade
        if grade == "A":
            grade_badge = '<span class="badge-A">A</span>'
        elif grade == "B":
            grade_badge = '<span class="badge-B">B</span>'
        else:
            grade_badge = '<span class="badge-C">C</span>'
        st.markdown(f"""
        <div style="border-bottom:1px solid #eee; padding:0.5rem 0;">
            <strong>{commerçant}</strong> – {produit} {grade_badge}<br>
            <small>Origine : {origine} | Destination : {destination} | Le {horodatage[:10]}</small>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("Aucune certification enregistrée.")
st.markdown('</div>', unsafe_allow_html=True)