import hashlib
import json
import qrcode
from PIL import Image
import io
import os
from core.logger import logger
from core.config import PROJECT_DIR

def generer_hash(donnees: dict) -> str:
    contenu = json.dumps(donnees, sort_keys=True)
    return hashlib.sha256(contenu.encode()).hexdigest()

def generer_qr(donnees: dict, dossier_sortie="static/qr_codes") -> str:
    signature = generer_hash(donnees)
    payload = {"data": donnees, "signature": signature}
    contenu_qr = json.dumps(payload)
    img = qrcode.make(contenu_qr)
    os.makedirs(dossier_sortie, exist_ok=True)
    nom_fichier = f"{signature[:10]}.png"
    chemin = os.path.join(dossier_sortie, nom_fichier)
    img.save(chemin)
    logger.info(f"QR code généré : {chemin}")
    return chemin

def decode_qr(chemin_image: str) -> dict:
    from pyzbar.pyzbar import decode
    try:
        img = Image.open(chemin_image)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        decoded_objects = decode(img)
        if not decoded_objects:
            raise ValueError("Aucun QR code trouvé dans l'image.")
        data = decoded_objects[0].data.decode("utf-8")
        return json.loads(data)
    except Exception as e:
        logger.error(f"Erreur décodage QR : {e}")
        raise

def decode_qr_from_bytes(image_bytes: bytes) -> dict:
    """Décode un QR code à partir d'un flux d'octets (ex: upload Streamlit)"""
    from pyzbar.pyzbar import decode
    try:
        img = Image.open(io.BytesIO(image_bytes))
        if img.mode != 'RGB':
            img = img.convert('RGB')
        decoded_objects = decode(img)
        if not decoded_objects:
            raise ValueError("Aucun QR code trouvé dans l'image.")
        data = decoded_objects[0].data.decode("utf-8")
        return json.loads(data)
    except Exception as e:
        logger.error(f"Erreur décodage QR depuis bytes : {e}")
        raise

def verifier_certificat(payload: dict) -> (bool, dict):
    donnees = payload.get("data")
    signature_recue = payload.get("signature")
    signature_calculee = generer_hash(donnees)
    if signature_calculee == signature_recue:
        return True, donnees
    else:
        return False, None