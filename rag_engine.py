import os
import glob
from PyPDF2 import PdfReader
import chromadb
from chromadb.utils import embedding_functions
import google.generativeai as genai
import config
from logger import logger

genai.configure(api_key=config.API_KEY)
model_texte = genai.GenerativeModel('models/gemini-2.5-flash')

# Initialisation ChromaDB
chroma_client = chromadb.PersistentClient(path="vectordb")
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
collection = chroma_client.get_or_create_collection(name="zlecaf", embedding_function=sentence_transformer_ef)

def _extraire_texte_pdfs(dossier="data"):
    texte_total = ""
    for fichier in os.listdir(dossier):
        if fichier.endswith(".pdf"):
            chemin = os.path.join(dossier, fichier)
            reader = PyPDF2.PdfReader(chemin)
            for page in reader.pages:
                texte = page.extract_text()
                if texte:
                    texte_total += texte + "\n"
    return texte_total

def _decouper_en_paragraphes(texte):
    paragraphes = [p.strip() for p in texte.split("\n\n") if len(p.strip()) > 100]
    return paragraphes

def initialiser_rag():
    # Ne réindexe que si la collection est vide
    if collection.count() > 0:
        return
    texte = _extraire_texte_pdfs(config.DATA_DIR)
    paragraphes = _decouper_en_paragraphes(texte)
    ids = [f"p{i}" for i in range(len(paragraphes))]
    collection.add(documents=paragraphes, ids=ids)

def repondre_question(question: str) -> str:
    # Recherche contexte
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
    try:
        reponse = modele_texte.generate_content(prompt)
        return reponse.text
    except Exception as e:
        logger.error(f"Erreur appel Gemini RAG : {e}")
        return "Désolé, l'assistant juridique est momentanément indisponible."
    return reponse.text
