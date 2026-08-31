"""Deep learning inference service.

Loads the active model (defined in ml/config.py) once and exposes a prediction
function that mirrors the preprocessing used during training
(cancer_detection.py): images are resized / rescaled and passed through the
binary sigmoid head (0 = Benign, 1 = Malignant). If the active model in the
config changes (name, file or image size), this service automatically follows
it — including when the training pipeline records a new ModelTraining entry.
"""

from __future__ import annotations

import numpy as np
from PIL import Image

from . import config

# Importing keras/tensorflow is deferred to avoid a heavy import at module
# load. The model is loaded lazily on first use.
_model = None
_model_source = None


def _get_model():
    """Load (and cache) the Keras model pointed to by the central config."""
    global _model, _model_source

    path = str(config.MODEL_PATH)
    if _model is None or _model_source != path:
        from tensorflow.keras.models import load_model

        _model = load_model(path, compile=False)
        _model_source = path
    return _model


def preprocess_image(image: Image.Image) -> np.ndarray:
    """Convert a PIL image into a (1, N, N, 3) float32 array in [0,1]."""
    image = image.convert("RGB").resize(config.IMG_SIZE)
    arr = np.asarray(image, dtype="float32") / 255.0
    arr = np.expand_dims(arr, axis=0)
    return arr


def predict(image: Image.Image) -> dict:
    """Run inference and return a normalized prediction result."""
    model = _get_model()
    array = preprocess_image(image)
    raw = float(model.predict(array, verbose=0)[0][0])

    probability = float(raw)
    prediction = "Malignant" if probability >= 0.5 else "Benign"

    # Report confidence relative to the predicted class.
    confidence = probability if prediction == "Malignant" else 1.0 - probability

    return {
        "prediction": prediction,
        "confidence": round(confidence * 100, 2),
        "probability": round(probability, 4),
    }
