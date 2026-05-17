import tensorflow as tf
import os

def load_datasets(base_dir="dataset", batch_size=32):
    train_dir = os.path.join(base_dir, "train")
    val_dir = os.path.join(base_dir, "validation")

    # 1. Chargement brut (sans transformations)
    train_ds_raw = tf.keras.preprocessing.image_dataset_from_directory(
        train_dir,
        image_size=(224, 224),
        batch_size=batch_size,
        label_mode='categorical'
    )
    val_ds_raw = tf.keras.preprocessing.image_dataset_from_directory(
        val_dir,
        image_size=(224, 224),
        batch_size=batch_size,
        label_mode='categorical'
    )

    # 2. Récupération des noms de classes (à partir du dataset brut)
    class_names = train_ds_raw.class_names

    # 3. Normalisation (pixels de 0-255 → 0-1)
    norm = tf.keras.layers.Rescaling(1./255)
    train_ds = train_ds_raw.map(lambda x, y: (norm(x), y))
    val_ds = val_ds_raw.map(lambda x, y: (norm(x), y))

    # 4. Optimisations (cache, shuffle, prefetch)
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

    return train_ds, val_ds, class_names