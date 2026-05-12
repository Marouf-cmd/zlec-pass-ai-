
from training.model import build_model

num_classes = 15  # à ajuster selon vos classes (café, cacao, céréales x 3)
model = build_model(num_classes)
model.summary()