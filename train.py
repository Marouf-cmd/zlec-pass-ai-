import tensorflow as tf
import os
from training.data_loader import load_datasets
from training.model import build_model

# Vérification que TensorFlow voit le GPU (optionnel)
print("TensorFlow version :", tf.__version__)
print("GPU disponible :", tf.config.list_physical_devices('GPU'))

# 1. Chargement des données
print("Chargement des datasets...")
train_ds, val_ds, class_names = load_datasets(batch_size=32)  # ajustez batch_size selon votre RAM

# 2. Sauvegarde des noms de classes
with open('class_names.txt', 'w') as f:
    for name in class_names:
        f.write(name + '\n')
print(f"Classes sauvegardées dans class_names.txt : {class_names}")

# 3. Construction du modèle
print("Construction du modèle...")
model = build_model(len(class_names))
model.summary()

# 4. Callbacks
callbacks = [
    tf.keras.callbacks.EarlyStopping(patience=5, restore_best_weights=True, verbose=1),
    tf.keras.callbacks.ModelCheckpoint('best_model.h5', save_best_only=True, verbose=1)
]

# 5. Entraînement
print("Début de l'entraînement...")
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=30,
    callbacks=callbacks,
    verbose=1
)

# 6. Sauvegarde du modèle final
model.save('final_model.h5')
print("Entraînement terminé. Modèle final sauvegardé sous final_model.h5")