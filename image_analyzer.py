import hashlib
import json
import os
import google.generativeai as genai
from PIL import Image
import config

genai.configure(api_key=config.API_KEY)
model = genai.GenerativeModel('models/gemini-2.5-flash')

def _hash_image(chemin_image: str) -> str:
    with open(chemin_image, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def _cache_get(hash_img):
    chemin_cache = os.path.join(config.CACHE_DIR, f"{hash_img}.json")
    if os.path.exists(chemin_cache):
        with open(chemin_cache, "r") as f:
            return json.load(f)
    return None

def _cache_set(hash_img, resultat):
    chemin_cache = os.path.join(config.CACHE_DIR, f"{hash_img}.json")
    with open(chemin_cache, "w") as f:
        json.dump(resultat, f)

def analyze_product(chemin_image: str) -> dict:
    h = _hash_image(chemin_image)
    cached = _cache_get(h)
    if cached:
        return cached

    img = Image.open(chemin_image)
    prompt = """
    Tu es un expert en contrôle qualité de produits agricoles africains.
    Analyse cette image. Détermine le type de produit (café, cacao, céréales, autre).
    Attribue un grade : A (excellent), B (bon), C (médiocre).
    Réponds UNIQUEMENT en JSON avec les clés "produit" et "grade".
    """
    response = model.generate_content([prompt, img])
    try:
        resultat = json.loads(response.text)
    except:
        resultat = {"produit": "inconnu", "grade": "C"}
    _cache_set(h, resultat)
    return resultat
