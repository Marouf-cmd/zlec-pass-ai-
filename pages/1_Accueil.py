import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from core.database import get_certifications, get_top_commercants
from core.config import PAYS_ISO
from fpdf import FPDF
import tempfile
from core.style import inject_css
from core.theme_utils import theme_toggle

inject_css()

# Vérification de l'authentification
if 'user' not in st.session_state:
    st.error("❌ Veuillez vous connecter pour accéder au tableau de bord.")
    st.stop()

# Barre latérale avec déconnexion et thème
with st.sidebar:
    theme_toggle()
    st.markdown("---")
    if st.button("🚪 Se déconnecter"):
        del st.session_state.user
        st.switch_page("pages/0_Login.py")

st.markdown('<h1 class="main-header"><i class="fas fa-chart-line"></i> Tableau de bord ZLECAf</h1>', unsafe_allow_html=True)

# ... (le reste du code inchangé)
# Récupération des données
certifications = get_certifications()
top_commercants = get_top_commercants(10)

if certifications:
    df = pd.DataFrame(certifications, columns=["produit", "grade", "origine", "destination", "economie", "date", "commercant"])
    df['date'] = pd.to_datetime(df['date'])
    
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()
    
    # Mémorisation des dates
    if 'start_date' not in st.session_state:
        st.session_state.start_date = min_date
    if 'end_date' not in st.session_state:
        st.session_state.end_date = max_date
    
    st.markdown("### 📅 Filtrer par période")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Date de début", st.session_state.start_date, min_value=min_date, max_value=max_date)
    with col2:
        end_date = st.date_input("Date de fin", st.session_state.end_date, min_value=min_date, max_value=max_date)
    
    if start_date != st.session_state.start_date or end_date != st.session_state.end_date:
        st.session_state.start_date = start_date
        st.session_state.end_date = end_date
        st.rerun()
    
    if start_date <= end_date:
        mask = (df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)
        df_filtered = df[mask]
    else:
        st.error("La date de début doit être antérieure à la date de fin.")
        df_filtered = df
    
    # Métriques
    col_met1, col_met2, col_met3, col_met4 = st.columns(4)
    with col_met1:
        st.metric("📦 Certifications", len(df_filtered))
    with col_met2:
        st.metric("👥 Commerçants", len(df_filtered['commercant'].unique()))
    with col_met3:
        st.metric("🌾 Produits", len(df_filtered['produit'].unique()))
    with col_met4:
        st.metric("🌍 Pays d'origine", len(df_filtered['origine'].unique()))
    
    st.markdown("---")
    
    # Graphiques
    evolution = df_filtered.groupby(df_filtered['date'].dt.to_period('M')).size().reset_index(name='count')
    evolution['date'] = evolution['date'].astype(str)
    fig_evol = px.line(evolution, x='date', y='count', title="📈 Évolution mensuelle des certifications")
    st.plotly_chart(fig_evol, use_container_width=True)
    
    col_left, col_right = st.columns(2)
    with col_left:
        fig_produit = px.pie(df_filtered, names='produit', title="🍱 Répartition par produit")
        st.plotly_chart(fig_produit, use_container_width=True)
    with col_right:
        grade_counts = df_filtered.groupby('grade').size().reset_index(name='count')
        fig_grade = px.bar(grade_counts, x='grade', y='count', title="⭐ Qualité des produits",
                          color='grade', color_discrete_map={'A': '#2a9d2a', 'B': '#f4b942', 'C': '#e74c3c'})
        st.plotly_chart(fig_grade, use_container_width=True)
    
    pays_counts = df_filtered['origine'].value_counts().reset_index()
    pays_counts.columns = ['pays', 'count']
    fig_pays = px.bar(pays_counts.head(10), x='pays', y='count', title="🏆 Top 10 pays d'origine")
    st.plotly_chart(fig_pays, use_container_width=True)
    
    # Carte choropleth
    if not pays_counts.empty:
        pays_counts['code'] = pays_counts['pays'].map(PAYS_ISO)
        pays_counts = pays_counts.dropna(subset=['code'])
        if not pays_counts.empty:
            fig_map = px.choropleth(pays_counts, locations='code', color='count',
                                    hover_name='pays', color_continuous_scale='Greens',
                                    title="🌍 Certifications par pays d'origine")
            st.plotly_chart(fig_map, use_container_width=True)
    
    # Flux Sankey
    st.markdown("### ✈️ Flux de certification entre pays")
    flux = df_filtered.groupby(['origine', 'destination']).size().reset_index(name='count')
    if not flux.empty:
        nodes = list(set(flux['origine']).union(set(flux['destination'])))
        node_id = {node: i for i, node in enumerate(nodes)}
        fig_sankey = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=nodes,
            ),
            link=dict(
                source=[node_id[o] for o in flux['origine']],
                target=[node_id[d] for d in flux['destination']],
                value=flux['count'],
            )
        )])
        fig_sankey.update_layout(title="Flux d'exportations (origine → destination)", font_size=10)
        st.plotly_chart(fig_sankey, use_container_width=True)
    else:
        st.info("Aucune donnée de flux disponible.")
    
    # Téléchargements
    st.markdown("---")
    st.subheader("📥 Export des données")
    col_csv, col_html, col_pdf = st.columns(3)
    with col_csv:
        csv_data = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button("📄 CSV", data=csv_data, file_name="certifications.csv", mime="text/csv")
    with col_html:
        html_report = f"""
        <html>
        <head><title>Rapport ZLECAf</title></head>
        <body>
        <h1>Rapport des certifications</h1>
        <p>Généré le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>Période du {start_date} au {end_date}</p>
        {df_filtered.to_html()}
        </body>
        </html>
        """
        st.download_button("📄 HTML", data=html_report, file_name="rapport.html", mime="text/html")
    with col_pdf:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Rapport ZLECAf", ln=1, align="C")
        pdf.ln(10)
        pdf.set_font("Arial", size=10)
        pdf.cell(200, 10, txt=f"Généré le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=1)
        pdf.cell(200, 10, txt=f"Période : {start_date} au {end_date}", ln=1)
        pdf.ln(5)
        for idx, row in df_filtered.head(20).iterrows():
            ligne = f"{row['produit']} - {row['grade']} - {row['origine']} -> {row['destination']}"
            pdf.cell(200, 8, txt=ligne, ln=1)
        if len(df_filtered) > 20:
            pdf.cell(200, 8, txt=f"... et {len(df_filtered)-20} autres lignes", ln=1)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            pdf.output(tmp.name)
            with open(tmp.name, "rb") as f:
                pdf_data = f.read()
        st.download_button("📄 PDF", data=pdf_data, file_name="rapport.pdf", mime="application/pdf")
    
    # Classement
    st.markdown("---")
    st.subheader("🏅 Classement des commerçants")
    if top_commercants:
        df_top = pd.DataFrame(top_commercants, columns=["Nom", "Score", "Niveau"])
        st.dataframe(df_top, use_container_width=True, hide_index=True)
    else:
        st.info("Aucun commerçant enregistré.")
else:
    st.info("Aucune donnée de certification pour le moment. Revenez plus tard.")