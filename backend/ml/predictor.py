"""Deep learning inference service.

Loads the pre-trained CancerNet CNN model once and exposes a prediction
function that mirrors the preprocessing used during training
(cancer_detection.py): images are resized to 50x50, rescaled to [0,1] and
passed through the binary sigmoid head (0 = Benign, 1 = Malignant).
"""

from __future__ import annotations

import os

import numpy as np
from PIL import Image

# Importing keras/tensorflow is deferred to avoid a heavy import at module
# load. The model is loaded lazily on first use.
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "CancerNet_Model.h5")

IMG_SIZE = (50, 50)

# Class labels: IDC_negative -> Benign, IDC_positive -> Malignant
CLASS_LABELS = {0: "Benign", 1: "Malignant"}

_model = None


def _get_model():
    """Load and cache the Keras model."""
    global _model
    if _model is None:
        from tensorflow.keras.models import load_model

        _model = load_model(MODEL_PATH, compile=False)
    return _model


def preprocess_image(image: Image.Image) -> np.ndarray:
    """Convert a PIL image into a (1, 50, 50, 3) float32 array in [0,1]."""
    image = image.convert("RGB").resize(IMG_SIZE)
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
