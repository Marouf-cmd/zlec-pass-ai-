from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2

def build_model(num_classes):
    """
    Construit un modèle de classification par transfert learning avec MobileNetV2.
    """
    base = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    base.trainable = False   # on gèle les poids pré-entraînés

    model = models.Sequential([
        base,
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.2),
        layers.Dense(128, activation='relu'),
        layers.Dense(num_classes, activation='softmax')
    ])

    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    return model