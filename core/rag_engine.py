import os
from PyPDF2 import PdfReader
import chromadb
from chromadb.utils import embedding_functions
from google import genai
from core.config import API_KEY, DATA_DIR
from core.logger import logger
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent

# Initialisation du client Gemini (nouvelle API)
client = genai.Client(api_key=API_KEY)

# ChromaDB (inchangé)
chroma_client = chromadb.PersistentClient(path=os.path.join(PROJECT_DIR, "vectordb"))
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
collection = chroma_client.get_or_create_collection(name="zlecaf", embedding_function=sentence_transformer_ef)

def _extraire_texte_pdfs(dossier=DATA_DIR):
    texte_total = ""
    if not os.path.exists(dossier):
        logger.warning(f"Dossier {dossier} inexistant")
        return ""
    for fichier in os.listdir(dossier):
        if fichier.endswith(".pdf"):
            chemin = os.path.join(dossier, fichier)
            try:
                reader = PdfReader(chemin)
                for page in reader.pages:
                    texte = page.extract_text()
                    if texte:
                        texte_total += texte + "\n"
            except Exception as e:
                logger.error(f"Erreur lecture PDF {fichier}: {e}")
    return texte_total

def _decouper_en_paragraphes(texte):
    return [p.strip() for p in texte.split("\n\n") if len(p.strip()) > 100]

def initialiser_rag():
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
    return """📋 **Points de contrôle génériques (mode dégradé)** :

- Vérifier le certificat d'origine ZLECAf
- Inspection visuelle des lots (qualité, étiquetage)
- Conformité aux normes sanitaires et phytosanitaires
- Contrôle des documents de transport
- Vérification des taxes et droits de douane applicables

Pour une réponse plus précise, veuillez consulter un expert douanier."""