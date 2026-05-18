import streamlit as st

def init_theme():
    """Initialise le thème dans session_state et applique la classe CSS."""
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'
    
    theme_class = 'dark-theme' if st.session_state.theme == 'dark' else ''
    # Injecter un petit script JavaScript pour ajouter la classe au body
    st.markdown(f"""
    <script>
        document.body.className = '{theme_class}';
    </script>
    """, unsafe_allow_html=True)

def theme_toggle():
    """Affiche un bouton dans la sidebar pour basculer le thème."""
    cols = st.columns([1, 4])
    with cols[0]:
        icon = "🌙" if st.session_state.theme == 'light' else "☀️"
        if st.button(icon, help="Changer de thème (clair/sombre)"):
            st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'
            st.rerun()