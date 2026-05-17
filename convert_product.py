import sys
import tensorflow as tf

if len(sys.argv) != 2:
    print("Usage: python convert_product.py <produit>")
    sys.exit(1)

product = sys.argv[1]   # ex: cafe, cacao, mais, sorgho, riz

# Charger le modèle Keras entraîné
model = tf.keras.models.load_model(f'final_model_{product}.h5')

# Créer le convertisseur TFLite
converter = tf.lite.TFLiteConverter.from_keras_model(model)

# (Optionnel) Pour optimiser la taille, décommente la ligne suivante
# converter.optimizations = [tf.lite.Optimize.DEFAULT]

# Convertir
tflite_model = converter.convert()

# Sauvegarder le modèle .tflite
with open(f'model_{product}.tflite', 'wb') as f:
    f.write(tflite_model)

print(f"✅ TFLite prêt pour {product} -> model_{product}.tflite")