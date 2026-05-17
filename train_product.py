import sys
import tensorflow as tf
from training.data_loader import load_datasets
from training.model import build_model

if len(sys.argv) != 2:
    print("Usage: python train_product.py <produit>")
    sys.exit(1)

product = sys.argv[1]
base_dir = f"dataset_{product}"

train_ds, val_ds, class_names = load_datasets(base_dir=base_dir, batch_size=32)

with open(f'class_names_{product}.txt', 'w') as f:
    for name in class_names:
        f.write(name + '\n')

model = build_model(len(class_names))
model.summary()

cb = [
    tf.keras.callbacks.EarlyStopping(patience=5, restore_best_weights=True),
    tf.keras.callbacks.ModelCheckpoint(f'best_model_{product}.h5', save_best_only=True)
]

model.fit(train_ds, validation_data=val_ds, epochs=30, callbacks=cb)
model.save(f'final_model_{product}.h5')
print(f"Entraînement terminé pour {product}.")