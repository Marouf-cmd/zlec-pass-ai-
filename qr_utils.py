import hashlib
import json
import qrcode
from PIL import Image
import os

def generer_hash(donnees: dict) -> str:
    contenu = json.dumps(donnees, sort_keys=True)
    return hashlib.sha256(contenu.encode()).hexdigest()

def generer_qr(donnees: dict, dossier_sortie="static/qr_codes") -> str:
    # Générer le hash
    signature = generer_hash(donnees)
    # Combiner données et signature dans un payload
    payload = {"data": donnees, "signature": signature}
    contenu_qr = json.dumps(payload)
    # Créer le QR code
    img = qrcode.make(contenu_qr)
    os.makedirs(dossier_sortie, exist_ok=True)
    nom_fichier = f"{signature[:10]}.png"
    chemin = os.path.join(dossier_sortie, nom_fichier)
    img.save(chemin)
    return chemin

def decode_qr(chemin_image: str) -> dict:
    # Nécessite pyzbar et Pillow
    from pyzbar.pyzbar import decode
    img = Image.open(chemin_image)
    decoded_objects = decode(img)
    if not decoded_objects:
        raise ValueError("Aucun QR code trouvé dans l'image.")
    data = decoded_objects[0].data.decode("utf-8")
    return json.loads(data)

def verifier_certificat(payload: dict) -> (bool, dict):
    donnees = payload.get("data")
    signature_recue = payload.get("signature")
    signature_calculee = generer_hash(donnees)
    if signature_calculee == signature_recue:
        return True, donnees
    else:
        return False, None
