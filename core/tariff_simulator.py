import json
import os
from core.config import PAYS_ZLECAF
from core.logger import logger
from pathlib import Path

# Chemins
PROJECT_DIR = Path(__file__).resolve().parent.parent
CACHE_DIR = os.path.join(PROJECT_DIR, "cache")
os.makedirs(CACHE_DIR, exist_ok=True)
CHEMIN_TARIFS = os.path.join(CACHE_DIR, "tarifs.json")

def _extraire_et_sauvegarder():
    """Crée le fichier tarifs.json avec les valeurs par défaut."""
    tarifs = {
        "cafe": {"standard": 20, "A_B": 0, "C": 5},
        "cacao": {"standard": 15, "A_B": 0, "C": 3},
        "mais": {"standard": 12, "A_B": 0, "C": 2},
        "sorgho": {"standard": 12, "A_B": 0, "C": 2},
        "riz": {"standard": 12, "A_B": 0, "C": 2},
    }
    with open(CHEMIN_TARIFS, "w") as f:
        json.dump(tarifs, f, indent=4)
    logger.info("Fichier tarifs.json créé avec les valeurs par défaut.")
    return tarifs

def charger_tarifs():
    if os.path.exists(CHEMIN_TARIFS):
        with open(CHEMIN_TARIFS, "r") as f:
            return json.load(f)
    else:
        return _extraire_et_sauvegarder()

def simuler_tarif(produit: str, grade: str, origine: str, destination: str) -> str:
    # Vérifier que les deux pays sont membres ZLECAf
    if origine not in PAYS_ZLECAF or destination not in PAYS_ZLECAF:
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