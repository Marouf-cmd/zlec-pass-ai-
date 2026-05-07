import json
import os
from core.config import PAYS_ZLECAF, DATA_DIR, API_KEY   # import explicite
from core import rag_engine
import google.generativeai as genai
from core.logger import logger
from pathlib import Path

# Définir les chemins (utilise ceux de config ou les tiens)
PROJECT_DIR = Path(__file__).resolve().parent.parent
CACHE_DIR = os.path.join(PROJECT_DIR, "cache")
os.makedirs(CACHE_DIR, exist_ok=True)
CHEMIN_TARIFS = os.path.join(CACHE_DIR, "tarifs.json")

def _extraire_et_sauvegarder():
    texte = rag_engine._extraire_texte_pdfs(DATA_DIR)   # plus de config.
    # Si aucun texte trouvé, on prend directement les valeurs par défaut
    if not texte.strip():
        tarifs = {
            "cafe": {"standard": 20, "A_B": 0, "C": 5},
            "cacao": {"standard": 15, "A_B": 0, "C": 3},
            "cereales": {"standard": 10, "A_B": 0, "C": 2},
        }
        with open(CHEMIN_TARIFS, "w") as f:
            json.dump(tarifs, f)
        return tarifs

    # Sinon, on interroge l'IA
    genai.configure(api_key=API_KEY)   # plus de config.
    model_texte = genai.GenerativeModel('models/gemini-2.5-flash')
    prompt = f"""À partir du texte réglementaire suivant, extrais les droits de douane... (le reste du prompt)"""
    reponse = model.generate_content(prompt)
    try:
        tarifs = json.loads(reponse.text)
    except Exception as e:
        tarifs = {
            "cafe": {"standard": 20, "A_B": 0, "C": 5},
            "cacao": {"standard": 15, "A_B": 0, "C": 3},
            "cereales": {"standard": 10, "A_B": 0, "C": 2},
        }
        logger.error(f"Erreur parsing tarifs IA : {e}")
    with open(CHEMIN_TARIFS, "w") as f:
        json.dump(tarifs, f)
    return tarifs

def charger_tarifs():
    if os.path.exists(CHEMIN_TARIFS):
        with open(CHEMIN_TARIFS, "r") as f:
            return json.load(f)
    else:
        return _extraire_et_sauvegarder()

def simuler_tarif(produit: str, grade: str, origine: str, destination: str) -> str:
    # Vérifier que les deux pays sont ZLECAf
    if origine not in PAYS_ZLECAF or destination not in PAYS_ZLECAF:   # plus de config.
        return "Un des pays n'est pas membre ZLECAf. Tarif standard non simulé."
    tarifs = charger_tarifs()
    prod = produit.lower().strip()
    if prod not in tarifs:
        return f"Produit '{produit}' non supporté dans la base tarifaire."
    t = tarifs[prod]
    standard = t["standard"]
    if grade.upper() in ["A", "B"]:
        taux = t["A_B"]
    else:
        taux = t["C"]
    economie = standard - taux
    if economie > 0:
        return f"Tarif standard : {standard}%. Tarif ZLECAf appliqué : {taux}%. Économie : {economie} points de pourcentage."
    else:
        return f"Tarif standard : {standard}%. Aucune réduction pour ce produit/grade."