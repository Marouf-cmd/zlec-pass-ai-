import os
import cv2

SIZE = (224, 224)

# Parcourt tous les dossiers commençant par "dataset_"
for base in [d for d in os.listdir('.') if d.startswith('dataset_') and os.path.isdir(d)]:
    print(f"Traitement de {base}...")
    for split in ["train", "validation"]:
        split_path = os.path.join(base, split)
        if not os.path.exists(split_path):
            continue
        for classe in os.listdir(split_path):
            class_path = os.path.join(split_path, classe)
            if not os.path.isdir(class_path):
                continue
            print(f"  -> {split}/{classe}")
            for img_name in os.listdir(class_path):
                img_path = os.path.join(class_path, img_name)
                try:
                    img = cv2.imread(img_path)
                    if img is None:
                        print(f"      Impossible de lire {img_name}, ignoré.")
                        continue
                    img = cv2.resize(img, SIZE)
                    cv2.imwrite(img_path, img)
                except Exception as e:
                    print(f"      Erreur sur {img_path}: {e}")
    print(f"Terminé pour {base}.\n")

print("✅ Redimensionnement terminé pour tous les datasets.")