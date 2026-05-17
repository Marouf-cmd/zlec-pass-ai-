import os
from PyPDF2 import PdfReader   # import correct
import chromadb
from chromadb.utils import embedding_functions
import google.generativeai as genai
from core.config import API_KEY, DATA_DIR   # plus besoin de config.
from core.logger import logger
from pathlib import Path

# Chemin racine du projet
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Configuration Gemini
genai.configure(api_key=API_KEY)
model_texte = genai.GenerativeModel('models/gemini-2.5-flash')

# Client ChromaDB
chroma_client = chromadb.PersistentClient(path=os.path.join(PROJECT_DIR, "vectordb"))
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
collection = chroma_client.get_or_create_collection(name="zlecaf", embedding_function=sentence_transformer_ef)

def _extraire_texte_pdfs(dossier=DATA_DIR):
    """Extrait tout le texte des PDFs dans le dossier donné"""
    texte_total = ""
    if not os.path.exists(dossier):
        logger.warning(f"Dossier {dossier} inexistant")
        return ""
    for fichier in os.listdir(dossier):
        if fichier.endswith(".pdf"):
            chemin = os.path.join(dossier, fichier)
            try:
                reader = PdfReader(chemin)   # utilisation correcte de PdfReader
                for page in reader.pages:
                    texte = page.extract_text()
                    if texte:
                        texte_total += texte + "\n"
            except Exception as e:
                logger.error(f"Erreur lecture PDF {fichier}: {e}")
    return texte_total

def _decouper_en_paragraphes(texte):
    """Découpe en paragraphes de plus de 100 caractères"""
    paragraphes = [p.strip() for p in texte.split("\n\n") if len(p.strip()) > 100]
    return paragraphes

def initialiser_rag():
    """Initialise la base vectorielle si vide"""
    if collection.count() > 0:
        logger.info("Base vectorielle déjà initialisée")
        return
    texte = _extraire_texte_pdfs(DATA_DIR)
    if not texte.strip():
        logger.warning("Aucun texte extrait des PDFs")
        return
    paragraphes = _decouper_en_paragraphes(texte)
    ids = [f"p{i}" for i in range(len(paragraphes))]
    collection.add(documents=paragraphes, ids=ids)
    logger.info(f"Base vectorielle initialisée avec {len(paragraphes)} paragraphes")
def repondre_question(question: str) -> str:
    try:
        results = collection.query(query_texts=[question], n_results=3)
        contextes = results['documents'][0]
        contexte_texte = "\n\n".join(contextes)
        prompt = f"""Tu es un assistant juridique spécialiste des textes de la ZLECAf.
Réponds à la question en te basant UNIQUEMENT sur les extraits suivants.
Si la réponse ne s'y trouve pas, dis-le.

Extraits :
{contexte_texte}

Question : {question}
Réponse :"""
        reponse = model_texte.generate_content(prompt)
        return reponse.text
    except Exception as e:
        # Affiche l'erreur détaillée dans les logs (et dans l'interface)
        logger.error(f"Erreur complète : {e}", exc_info=True)
        return f"Erreur technique : {type(e).__name__} – {str(e)}"