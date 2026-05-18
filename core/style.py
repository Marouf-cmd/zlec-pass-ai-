import streamlit as st

def inject_css():
    st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        /* Global */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }
        .main {
            background: linear-gradient(135deg, #f5f7fa 0%, #eef2f5 100%);
        }
        /* Titres */
        h1, h2, h3, .main-header {
            font-family: 'Poppins', sans-serif;
            font-weight: 600;
            background: linear-gradient(120deg, #1e5f1e, #2a9d2a);
            background-clip: text;
            -webkit-background-clip: text;
            color: transparent;
            margin-bottom: 1rem;
        }
        /* Cartes */
        .card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(2px);
            border-radius: 24px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.02);
            padding: 1.8rem;
            margin: 1.2rem 0;
            transition: all 0.3s ease;
            border: 1px solid rgba(255,255,255,0.2);
        }
        .card:hover {
            transform: translateY(-4px);
            box-shadow: 0 20px 30px -12px rgba(0, 0, 0, 0.15);
            background: white;
        }
        /* Badges de grade */
        .badge-A {
            background: linear-gradient(135deg, #2a9d2a, #1e7a1e);
            color: white;
            padding: 0.2rem 0.8rem;
            border-radius: 40px;
            font-weight: 600;
            font-size: 0.8rem;
            display: inline-block;
        }
        .badge-B {
            background: linear-gradient(135deg, #f4b942, #e67e22);
            color: white;
            padding: 0.2rem 0.8rem;
            border-radius: 40px;
            font-weight: 600;
            font-size: 0.8rem;
        }
        .badge-C {
            background: linear-gradient(135deg, #e74c3c, #c0392b);
            color: white;
            padding: 0.2rem 0.8rem;
            border-radius: 40px;
            font-weight: 600;
            font-size: 0.8rem;
        }
        /* Boutons Streamlit personnalisés */
        .stButton > button {
            background: linear-gradient(90deg, #2a9d2a, #218c21);
            color: white;
            border: none;
            border-radius: 40px;
            padding: 0.5rem 1.8rem;
            font-weight: 500;
            transition: 0.2s;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .stButton > button:hover {
            background: linear-gradient(90deg, #1f7a1f, #1a661a);
            transform: scale(1.02);
            box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        }
        /* Inputs */
        .stTextInput > div > div > input, .stSelectbox > div > div > select {
            border-radius: 28px;
            border: 1px solid #ddd;
            padding: 0.5rem 1rem;
        }
        /* File uploader */
        .stFileUploader > div {
            border: 2px dashed #2a9d2a;
            border-radius: 28px;
            background: rgba(42,157,42,0.05);
        }
        /* Sidebar */
        .css-1d391kg {
            background: linear-gradient(180deg, #1a3c1a, #0f2b0f);
        }
        .sidebar .sidebar-content {
            background: transparent;
        }
        .sidebar .stSelectbox label, .sidebar .stTextInput label {
            color: #e0e0e0;
        }
        /* Layout responsive */
        @media (max-width: 768px) {
            .card { padding: 1rem; }
        }
        /* Métriques */
.metric-card {
    background: white;
    border-radius: 20px;
    padding: 1rem 1.2rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    text-align: center;
    transition: all 0.2s;
}
.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 20px -10px rgba(0,0,0,0.1);
}
.metric-value {
    font-size: 2rem;
    font-weight: 700;
    color: #2a9d2a;
}
.metric-label {
    font-size: 0.8rem;
    color: #666;
    text-transform: uppercase;
    letter-spacing: 1px;
}
/* Notifications */
.success-toast {
    background: #d4edda;
    color: #155724;
    border-left: 5px solid #2a9d2a;
    padding: 0.8rem;
    border-radius: 12px;
    margin: 0.5rem 0;
}
.error-toast {
    background: #f8d7da;
    color: #721c24;
    border-left: 5px solid #e74c3c;
    padding: 0.8rem;
    border-radius: 12px;
}
/* Tableau stylisé */
.data-table {
    width: 100%;
    border-collapse: collapse;
    background: white;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.03);
}
.data-table th {
    background: #f0f2f5;
    padding: 0.8rem;
    text-align: left;
    font-weight: 600;
}
.data-table td {
    padding: 0.8rem;
    border-bottom: 1px solid #eee;
}
/* QR code container */
.qr-container {
    background: white;
    border-radius: 20px;
    padding: 1rem;
    text-align: center;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
    /* ========== THÈME SOMBRE ========== */
.dark-theme {
    background-color: #121212;
    color: #e0e0e0;
}
.dark-theme .card {
    background: #1e1e1e;
    border-color: #333;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}
.dark-theme .stButton>button {
    background: #2a9d2a;
    color: white;
}
.dark-theme .stButton>button:hover {
    background: #1f7a1f;
}
.dark-theme .data-table th {
    background: #2c2c2c;
    color: #f0f0f0;
}
.dark-theme .data-table td {
    border-bottom-color: #333;
}
.dark-theme .stTextInput > div > div > input,
.dark-theme .stSelectbox > div > div > select {
    background-color: #2c2c2c;
    color: #e0e0e0;
    border-color: #555;
}
.dark-theme .stFileUploader > div {
    background: rgba(42,157,42,0.1);
    border-color: #2a9d2a;
}
/* Transition douce pour tout */
body, .card, .stButton>button, .stTextInput input, .stSelectbox select {
    transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
}
    </style>
    """, unsafe_allow_html=True)