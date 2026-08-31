"""Central model configuration (single source of truth).

Defines the active deep-learning model used by both the runtime inference
service (backend/ml/predictor.py) and the training pipeline
(ml/cancer_detection.py). To switch to a different model, change these values
(or set the corresponding environment variables) and the Model Performance
page, prediction service and training pipeline all pick it up automatically.
"""

from __future__ import annotations

import os
from pathlib import Path

# Directory that contains the .h5 model files (backend/ml/model).
MODEL_DIR = Path(__file__).resolve().parent / "model"

# The back-end can be pointed at an entirely different model directory/file
# via environment variables without editing code (useful in production).
ML_CONFIG = {
    "name": os.environ.get("ML_MODEL_NAME", "CancerNet"),
    "dataset_name": os.environ.get("ML_DATASET_NAME", "IDC_regular_ps50_idx5"),
    "model_file": os.environ.get("ML_MODEL_FILE", "CancerNet_Model.h5"),
    "image_size": int(os.environ.get("ML_IMAGE_SIZE", "50")),
    "classes": int(os.environ.get("ML_CLASSES", "2")),
    # Class labels in prediction order: index 0 = Benign, index 1 = Malignant.
    "labels": ["Benign", "Malignant"],
}

# Absolute path of the active model weights file. Supports either a bare
# filename stored inside MODEL_DIR or an absolute path to a .h5 on disk.
_model_file = ML_CONFIG["model_file"]
if os.path.isabs(_model_file):
    MODEL_PATH = Path(_model_file)
else:
    MODEL_PATH = MODEL_DIR / _model_file

# Image dimensions expected by the model, as a 2-tuple.
IMG_SIZE = (ML_CONFIG["image_size"], ML_CONFIG["image_size"])


def get_config() -> dict:
    """Return a copy of the active model configuration."""
    return dict(ML_CONFIG)
