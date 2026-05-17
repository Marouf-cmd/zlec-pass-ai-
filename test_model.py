import sys
import tensorflow.lite as tflite
import numpy as np
import cv2

if len(sys.argv) != 3:
    print("Usage: python test_model.py <produit> <image_path>")
    sys.exit(1)

product = sys.argv[1]          # ex: cafe
image_path = sys.argv[2]       # ex: dataset_cafe/train/cafe_A/07.jpg

# Charger le modèle TFLite
interpreter = tflite.Interpreter(model_path=f'model_{product}.tflite')
interpreter.allocate_tensors()
inp = interpreter.get_input_details()
out = interpreter.get_output_details()

# Charger les noms des classes
with open(f'class_names_{product}.txt') as f:
    classes = [l.strip() for l in f]

# Lire et prétraiter l'image
img = cv2.imread(image_path)
img = cv2.resize(img, (224, 224))
img = img.astype(np.float32) / 255.0
img = np.expand_dims(img, axis=0)   # ajoute la dimension batch

# Inférence
interpreter.set_tensor(inp[0]['index'], img)
interpreter.invoke()
pred = interpreter.get_tensor(out[0]['index'])[0]
idx = np.argmax(pred)
print(f"Classe: {classes[idx]}, Confiance: {pred[idx]:.2f}")