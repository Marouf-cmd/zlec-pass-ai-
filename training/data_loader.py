import tensorflow as tf
import os

def load_datasets(base_dir="dataset", batch_size=32):
    train_dir = os.path.join(base_dir, "train")
    val_dir = os.path.join(base_dir, "validation")

    if not os.path.exists(train_dir):
        raise FileNotFoundError(f"Le dossier d'entraînement {train_dir} est introuvable.")
    if not os.path.exists(val_dir):
        raise FileNotFoundError(f"Le dossier de validation {val_dir} est introuvable.")

    # 1. Chargement brut des datasets
    train_ds_raw = tf.keras.preprocessing.image_dataset_from_directory(
        train_dir,
        image_size=(224, 224),
        batch_size=batch_size,
        label_mode='categorical',
        shuffle=True,
        seed=42
    )
    val_ds_raw = tf.keras.preprocessing.image_dataset_from_directory(
        val_dir,
        image_size=(224, 224),
        batch_size=batch_size,
        label_mode='categorical',
        shuffle=False
    )

    # 2. Récupérer les noms des classes AVANT les transformations
    class_names = train_ds_raw.class_names

    # 3. Normalisation [0,1]
    normalisation = tf.keras.layers.Rescaling(1./255)
    train_ds = train_ds_raw.map(lambda x, y: (normalisation(x), y))
    val_ds = val_ds_raw.map(lambda x, y: (normalisation(x), y))

    # 4. Optimisations (cache, shuffle, prefetch)
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

    return train_ds, val_ds, class_names