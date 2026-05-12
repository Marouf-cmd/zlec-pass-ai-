import os
import cv2

BASE = "dataset"
SIZE = (224, 224)

for split in ["train", "validation"]:
    split_path = os.path.join(BASE, split)
    if not os.path.exists(split_path):
        print(f"Le dossier {split_path} n'existe pas, on ignore.")
        continue
    for classe in os.listdir(split_path):
        class_path = os.path.join(split_path, classe)
        if not os.path.isdir(class_path):
            continue
        print(f"Traitement de {class_path}")
        for img_name in os.listdir(class_path):
            img_path = os.path.join(class_path, img_name)
            if not img_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                continue
            try:
                img = cv2.imread(img_path)
                if img is None:
                    print(f"Impossible de lire {img_path}")
                    continue
                img = cv2.resize(img, SIZE)
                cv2.imwrite(img_path, img)
            except Exception as e:
                print(f"Erreur sur {img_path}: {e}")

print("Redimensionnement terminé.")