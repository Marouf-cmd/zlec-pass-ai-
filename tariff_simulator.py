import json
import os
import config
import rag_engine  # on utilise l'IA pour extraire les données une fois
import google.generativeai as genai

CHEMIN_TARIFS = os.path.join(config.CACHE_DIR, "tarifs.json")

def _extraire_et_sauvegarder():
    texte = rag_engine._extraire_texte_pdfs(config.DATA_DIR)
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
    genai.configure(api_key=config.API_KEY)
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    prompt = f"""À partir du texte réglementaire suivant, extrais les droits de douane... (le reste du prompt)"""
    reponse = model.generate_content(prompt)
    try:
        tarifs = json.loads(reponse.text)
    except:
        tarifs = {
            "cafe": {"standard": 20, "A_B": 0, "C": 5},
            "cacao": {"standard": 15, "A_B": 0, "C": 3},
            "cereales": {"standard": 10, "A_B": 0, "C": 2},
        }
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
    if origine not in config.PAYS_ZLECAF or destination not in config.PAYS_ZLECAF:
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
