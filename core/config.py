import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
DATA_DIR = os.path.join(PROJECT_DIR, "data")
CACHE_DIR = os.path.join(PROJECT_DIR, "cache")
LOG_DIR = os.path.join(PROJECT_DIR, "logs")
os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY non trouvée dans .env")

PAYS_ZLECAF = [
    "Afrique du Sud", "Algérie", "Angola", "Bénin", "Botswana", "Burkina Faso", "Burundi",
    "Cameroun", "Cap-Vert", "République centrafricaine", "Comores", "Congo", "RD Congo",
    "Côte d'Ivoire", "Djibouti", "Égypte", "Érythrée", "Eswatini", "Éthiopie", "Gabon",
    "Gambie", "Ghana", "Guinée", "Guinée-Bissau", "Guinée équatoriale", "Kenya", "Lesotho",
    "Liberia", "Libye", "Madagascar", "Malawi", "Mali", "Maroc", "Maurice", "Mauritanie",
    "Mozambique", "Namibie", "Niger", "Nigeria", "Ouganda", "Rwanda",
    "Sao Tomé-et-Principe", "Sénégal", "Seychelles", "Sierra Leone", "Somalie", "Soudan",
    "Soudan du Sud", "Tanzanie", "Tchad", "Togo", "Tunisie", "Zambie", "Zimbabwe"
]

# Correspondance pays → code ISO alpha-3 pour Plotly
PAYS_ISO = {
    "Afrique du Sud": "ZAF", "Algérie": "DZA", "Angola": "AGO", "Bénin": "BEN",
    "Botswana": "BWA", "Burkina Faso": "BFA", "Burundi": "BDI", "Cameroun": "CMR",
    "Cap-Vert": "CPV", "République centrafricaine": "CAF", "Comores": "COM",
    "Congo": "COG", "RD Congo": "COD", "Côte d'Ivoire": "CIV", "Djibouti": "DJI",
    "Égypte": "EGY", "Érythrée": "ERI", "Eswatini": "SWZ", "Éthiopie": "ETH",
    "Gabon": "GAB", "Gambie": "GMB", "Ghana": "GHA", "Guinée": "GIN",
    "Guinée-Bissau": "GNB", "Guinée équatoriale": "GNQ", "Kenya": "KEN",
    "Lesotho": "LSO", "Liberia": "LBR", "Libye": "LBY", "Madagascar": "MDG",
    "Malawi": "MWI", "Mali": "MLI", "Maroc": "MAR", "Maurice": "MUS",
    "Mauritanie": "MRT", "Mozambique": "MOZ", "Namibie": "NAM", "Niger": "NER",
    "Nigeria": "NGA", "Ouganda": "UGA", "Rwanda": "RWA", "Sao Tomé-et-Principe": "STP",
    "Sénégal": "SEN", "Seychelles": "SYC", "Sierra Leone": "SLE", "Somalie": "SOM",
    "Soudan": "SDN", "Soudan du Sud": "SSD", "Tanzanie": "TZA", "Tchad": "TCD",
    "Togo": "TGO", "Tunisie": "TUN", "Zambie": "ZMB", "Zimbabwe": "ZWE"
}
