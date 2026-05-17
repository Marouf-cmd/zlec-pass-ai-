from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2

def build_model(num_classes):
    """
    Construit un modèle de classification par transfert learning avec MobileNetV2.
    """
    # Charger MobileNetV2 pré-entraîné sur ImageNet, sans la tête de classification
    base = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    
    # Geler les poids du modèle de base (pas d'entraînement)
    base.trainable = False
    
    # Ajouter une tête de classification personnalisée
    model = models.Sequential([
        base,
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.2),
        layers.Dense(128, activation='relu'),
        layers.Dense(num_classes, activation='softmax')   # num_classes = 3 pour café, etc.
    ])
    
    # Compiler le modèle
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    return model