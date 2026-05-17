import numpy as np
import tensorflow.lite as tflite
import cv2
import os
from core.logger import logger

ML_DIR = os.path.join(os.path.dirname(__file__), 'ml')

# Caches pour éviter de recharger plusieurs fois
_interpreters = {}
_class_names = {}

def _load_model(product):
    """Charge le modèle TFLite et les noms de classes pour un produit donné."""
    if product not in _interpreters:
        model_path = os.path.join(ML_DIR, f'model_{product}.tflite')
        labels_path = os.path.join(ML_DIR, f'class_names_{product}.txt')
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Modèle {model_path} introuvable")
        if not os.path.exists(labels_path):
            raise FileNotFoundError(f"Fichier classes {labels_path} introuvable")
        
        interpreter = tflite.Interpreter(model_path=model_path)
        interpreter.allocate_tensors()
        _interpreters[product] = interpreter
        
        with open(labels_path, 'r') as f:
            _class_names[product] = [l.strip() for l in f]
    return _interpreters[product], _class_names[product]

def analyze_product(image_path, product="cafe"):
    """
    Analyse une image et retourne le grade (A, B, C) et le produit.
    product : 'cafe', 'cacao', 'mais', 'sorgho', 'riz'
    """
    try:
        interpreter, class_names = _load_model(product)
        inp = interpreter.get_input_details()
        out = interpreter.get_output_details()

        img = cv2.imread(image_path)
        if img is None:
            logger.error(f"Impossible de lire l'image : {image_path}")
            return {"produit": product, "grade": "C"}
        
        img = cv2.resize(img, (224, 224))
        img = img.astype(np.float32) / 255.0
        img = np.expand_dims(img, axis=0)

        interpreter.set_tensor(inp[0]['index'], img)
        interpreter.invoke()
        preds = interpreter.get_tensor(out[0]['index'])[0]
        idx = np.argmax(preds)
        conf = np.max(preds)
        classe = class_names[idx]          # ex: "cafe_A"
        # On suppose que le nom de la classe est sous la forme "produit_grade"
        _, grade = classe.split('_')
        logger.info(f"Analyse OK : {product} grade {grade} (confiance {conf:.2f})")
        return {"produit": product, "grade": grade}
    except Exception as e:
        logger.error(f"Erreur analyse : {e}")
        return {"produit": product, "grade": "C"}