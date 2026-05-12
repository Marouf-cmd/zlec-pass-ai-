import tensorflow as tf

# Charger le modèle Keras sauvegardé
model = tf.keras.models.load_model('final_model.h5')
print("Modèle chargé avec succès.")

# Convertir en TensorFlow Lite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()
print("Conversion terminée.")

# Sauvegarder le fichier .tflite
with open('model.tflite', 'wb') as f:
    f.write(tflite_model)

print("✅ Modèle TFLite prêt : model.tflite")