import streamlit as st

def inject_css():
    st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        /* Thème clair (défaut) */
        :root {
            --bg-app: #f5f7fa;
            --bg-card: white;
            --text-color: #111;
            --border: #ddd;
            --primary: #2a9d2a;
            --primary-dark: #1f7a1f;
            --sidebar-bg: linear-gradient(180deg, #1a3c1a, #0f2b0f);
        }
        body.dark-theme {
            --bg-app: #121212;
            --bg-card: #1e1e1e;
            --text-color: #e0e0e0;
            --border: #333;
            --sidebar-bg: linear-gradient(180deg, #0f1f0f, #050a05);
        }
        /* Styles généraux */
        .stApp {
            background-color: var(--bg-app);
            color: var(--text-color);
            transition: background-color 0.3s;
        }
        h1, h2, h3, .main-header {
            font-family: 'Poppins', sans-serif;
            font-weight: 600;
            background: linear-gradient(120deg, #1e5f1e, #2a9d2a);
            background-clip: text;
            -webkit-background-clip: text;
            color: transparent;
        }
        .card {
            background-color: var(--bg-card);
            border-radius: 24px;
            box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05);
            padding: 1.8rem;
            margin: 1.2rem 0;
            transition: all 0.3s;
            border: 1px solid var(--border);
        }
        .card:hover {
            transform: translateY(-4px);
        }
        .badge-A, .badge-B, .badge-C {
            padding: 0.2rem 0.8rem;
            border-radius: 40px;
            font-weight: 600;
            font-size: 0.8rem;
            display: inline-block;
        }
        .badge-A { background: linear-gradient(135deg, #2a9d2a, #1e7a1e); color: white; }
        .badge-B { background: linear-gradient(135deg, #f4b942, #e67e22); color: white; }
        .badge-C { background: linear-gradient(135deg, #e74c3c, #c0392b); color: white; }
        .stButton > button {
            background: linear-gradient(90deg, var(--primary), var(--primary-dark));
            color: white;
            border: none;
            border-radius: 40px;
            padding: 0.5rem 1.8rem;
            font-weight: 500;
            transition: all 0.2s;
        }
        .stButton > button:hover { transform: scale(1.02); }
        .stTextInput > div > div > input, .stSelectbox > div > div > select {
            border-radius: 28px;
            border: 1px solid var(--border);
            padding: 0.5rem 1rem;
            background-color: var(--bg-card);
            color: var(--text-color);
        }
        .stFileUploader > div {
            border: 2px dashed var(--primary);
            border-radius: 28px;
            background: rgba(42,157,42,0.05);
        }
        .css-1d391kg { background: var(--sidebar-bg); }
        .metric-card {
            background: var(--bg-card);
            border-radius: 20px;
            padding: 1rem 1.2rem;
            text-align: center;
        }
        .metric-value { font-size: 2rem; font-weight: 700; color: var(--primary); }
        .metric-label { font-size: 0.8rem; color: #666; text-transform: uppercase; }
        .success-toast {
            background: #d4edda;
            color: #155724;
            border-left: 5px solid var(--primary);
            padding: 0.8rem;
            border-radius: 12px;
        }
        .error-toast {
            background: #f8d7da;
            color: #721c24;
            border-left: 5px solid #e74c3c;
            padding: 0.8rem;
            border-radius: 12px;
        }
        .data-table {
            width: 100%;
            border-collapse: collapse;
            background: var(--bg-card);
            border-radius: 20px;
            overflow: hidden;
        }
        .data-table th { background: #f0f2f5; padding: 0.8rem; text-align: left; }
        .data-table td { padding: 0.8rem; border-bottom: 1px solid var(--border); }
        .qr-container {
            background: var(--bg-card);
            border-radius: 20px;
            padding: 1rem;
            text-align: center;
        }
        @media (max-width: 768px) { .card { padding: 1rem; } }
    </style>
    <script>
    const theme = new URLSearchParams(window.location.search).get('theme');
    if (theme === 'dark') {
        document.body.classList.add('dark-theme');
    }
    </script>
    """, unsafe_allow_html=True)
    