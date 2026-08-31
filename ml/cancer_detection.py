# ============================================================
# Breast Cancer Histology Image Classification using CNN
# CancerNet Model using TensorFlow / Keras
# ============================================================

# ============================================================
# 1. IMPORT LIBRARIES
# ============================================================

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

import tensorflow as tf

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping

# ============================================================
# 1b. MODEL CONFIGURATION (single source of truth)
# ============================================================
# The active model name, image size and save location are read from the
# central config in backend/ml/config.py so that training and the web-app
# prediction service always agree, and so the "Model Performance" page tracks
# whichever model is configured. Falls back to local defaults if the config
# module (or Django environment) is not reachable.

def _load_model_config():
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir, "backend"))
        from ml import config as _cfg

        return {
            "name": _cfg.ML_CONFIG["name"],
            "dataset_name": _cfg.ML_CONFIG["dataset_name"],
            "image_size": _cfg.ML_CONFIG["image_size"],
            "classes": _cfg.ML_CONFIG["classes"],
            "labels": list(_cfg.ML_CONFIG["labels"]),
            "model_file": _cfg.ML_CONFIG["model_file"],
            "model_path": str(_cfg.MODEL_PATH),
        }
    except Exception:  # noqa: BLE001 - fall back to sensible defaults
        return {
            "name": "CancerNet",
            "dataset_name": "IDC_regular_ps50_idx5",
            "image_size": 50,
            "classes": 2,
            "labels": ["Benign", "Malignant"],
            "model_file": "CancerNet_Model.h5",
            "model_path": os.path.join(
                os.path.dirname(__file__), os.pardir, "backend", "ml", "model", "CancerNet_Model.h5"
            ),
        }


ML_CFG = _load_model_config()
print("Active model config:", ML_CFG["name"], "-", ML_CFG["model_file"])

# ============================================================
# 2. DATASET PATH
# ============================================================

dataset_path = "IDC_regular_ps50_idx5"

# ============================================================
# 3. LOAD IMAGE PATHS AND LABELS
# ============================================================

image_paths = []
labels = []

# IDC_negative = 0
# IDC_positive = 1

for folder in os.listdir(dataset_path):

    folder_path = os.path.join(dataset_path, folder)

    if os.path.isdir(folder_path):

        for label_folder in ["0", "1"]:

            label_path = os.path.join(folder_path, label_folder)

            if os.path.exists(label_path):

                for image in os.listdir(label_path):

                    image_full_path = os.path.join(label_path, image)

                    image_paths.append(image_full_path)
                    labels.append(str(label_folder))

# Create dataframe

data = pd.DataFrame({
    "filename": image_paths,
    "label": labels
})

data = data.sample(20000, random_state=42)

print(data.head())

# ============================================================
# 4. TRAIN TEST SPLIT
# ============================================================

train_df, test_df = train_test_split(
    data,
    test_size=0.15,
    random_state=42,
    stratify=data["label"]
)

train_df, val_df = train_test_split(
    train_df,
    test_size=0.15,
    random_state=42,
    stratify=train_df["label"]
)

print("Training Samples :", len(train_df))
print("Validation Samples :", len(val_df))
print("Testing Samples :", len(test_df))

# ============================================================
# 5. IMAGE PREPROCESSING
# ============================================================

IMG_SIZE = ML_CFG["image_size"]
BATCH_SIZE = 32

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    zoom_range=0.2,
    horizontal_flip=True
)

test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_dataframe(
    dataframe=train_df,
    x_col="filename",
    y_col="label",
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="binary"
)

val_generator = test_datagen.flow_from_dataframe(
    dataframe=val_df,
    x_col="filename",
    y_col="label",
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="binary"
)

test_generator = test_datagen.flow_from_dataframe(
    dataframe=test_df,
    x_col="filename",
    y_col="label",
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="binary",
    shuffle=False
)

# ============================================================
# 6. BUILD CANCERNET CNN MODEL
# ============================================================

model = Sequential()

# First Convolution Layer
model.add(Conv2D(
    32,
    (3, 3),
    activation='relu',
    input_shape=(50, 50, 3)
))
model.add(MaxPooling2D(pool_size=(2, 2)))

# Second Convolution Layer
model.add(Conv2D(
    64,
    (3, 3),
    activation='relu'
))
model.add(MaxPooling2D(pool_size=(2, 2)))

# Third Convolution Layer
model.add(Conv2D(
    128,
    (3, 3),
    activation='relu'
))
model.add(MaxPooling2D(pool_size=(2, 2)))

# Flatten Layer
model.add(Flatten())

# Dense Layer
model.add(Dense(128, activation='relu'))

# Dropout to reduce overfitting
model.add(Dropout(0.5))

# Output Layer
model.add(Dense(1, activation='sigmoid'))

# ============================================================
# 7. COMPILE MODEL
# ============================================================

model.compile(
    optimizer=Adam(learning_rate=0.001),
    loss='binary_crossentropy',
    metrics=['accuracy']
)

model.summary()

# ============================================================
# 8. EARLY STOPPING
# ============================================================

early_stop = EarlyStopping(
    monitor='val_loss',
    patience=3,
    restore_best_weights=True
)

# ============================================================
# 9. TRAIN MODEL
# ============================================================

EPOCHS = 10

history = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=EPOCHS,
    callbacks=[early_stop]
)

# ============================================================
# 10. PLOT ACCURACY GRAPH
# ============================================================

plt.figure(figsize=(10, 5))

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])

plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')

plt.legend(['Train', 'Validation'])

plt.show()

# ============================================================
# 11. PLOT LOSS GRAPH
# ============================================================

plt.figure(figsize=(10, 5))

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])

plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')

plt.legend(['Train', 'Validation'])

plt.show()

# ============================================================
# 12. MODEL EVALUATION
# ============================================================

test_loss, test_accuracy = model.evaluate(test_generator)

print("\nTest Accuracy :", test_accuracy)
print("Test Loss :", test_loss)

# ============================================================
# 13. PREDICTIONS
# ============================================================

predictions = model.predict(test_generator)

predicted_classes = []

for pred in predictions:

    if pred > 0.5:
        predicted_classes.append(1)
    else:
        predicted_classes.append(0)

true_classes = test_generator.classes

# ============================================================
# 14. CONFUSION MATRIX
# ============================================================

cm = confusion_matrix(true_classes, predicted_classes)

print("\nConfusion Matrix")
print(cm)

# ============================================================
# 15. CLASSIFICATION REPORT
# ============================================================

report = classification_report(
    true_classes,
    predicted_classes
)

print("\nClassification Report")
print(report)

# ============================================================
# 16. SAVE MODEL
# ============================================================

# Save to the location that the web-app inference service loads from, and make
# sure the target directory exists.
os.makedirs(os.path.dirname(ML_CFG["model_path"]), exist_ok=True)
model.save(ML_CFG["model_path"])

print("\nModel Saved Successfully: {0}".format(ML_CFG["model_path"]))

# ============================================================
# 17. PERSIST TRAINING METRICS TO THE WEB APPLICATION DATABASE
# ============================================================
# Every time a model / dataset is trained, a ModelTraining record is created
# (or the latest one updated) so the "Model Performance" page always reflects
# the most recent run. This is optional: if the Django environment or database
# is unavailable, training still completes successfully.

def _derive_metrics(cm_array):
    """Compute macro metrics and per-class metrics from a 2x2 confusion matrix."""

    tn, fp = cm_array[0][0], cm_array[0][1]
    fn, tp = cm_array[1][0], cm_array[1][1]

    def safe(a, b):
        return float(a / b) if b else 0.0

    def calc(tp_c, fp_c, fn_c):
        precision = safe(tp_c, tp_c + fp_c)
        recall = safe(tp_c, tp_c + fn_c)
        f1 = safe(2 * precision * recall, precision + recall)
        return precision, recall, f1

    p_neg, r_neg, f1_neg = calc(tn, fp, fn)
    p_pos, r_pos, f1_pos = calc(tp, fn, fp)

    per_class = [
        {
            "class": "Benign",
            "precision": round(p_neg, 4),
            "recall": round(r_neg, 4),
            "f1": round(f1_neg, 4),
            "support": int(tn + fn),
        },
        {
            "class": "Malignant",
            "precision": round(p_pos, 4),
            "recall": round(r_pos, 4),
            "f1": round(f1_pos, 4),
            "support": int(tp + fp),
        },
    ]

    macro = {
        "precision": round((p_neg + p_pos) / 2, 4),
        "recall": round((r_neg + r_pos) / 2, 4),
        "f1": round((f1_neg + f1_pos) / 2, 4),
    }
    return per_class, macro


def _persist_training_metrics():
    import os

    try:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
        import django
        django.setup()

        from django.utils import timezone
        from predictions.models import ModelTraining

        per_class, macro = _derive_metrics(cm)

        ModelTraining.objects.create(
            name=ML_CFG["name"],
            version="v{0}".format(int(timezone.now().strftime("%Y%m%d%H%M"))),
            dataset_name=ML_CFG["dataset_name"],
            image_size=IMG_SIZE,
            classes=ML_CFG["classes"],
            epochs_total=EPOCHS,
            epochs_run=len(history.history.get("accuracy", [])),
            batch_size=BATCH_SIZE,
            train_samples=len(train_df),
            val_samples=len(val_df),
            test_samples=len(test_df),
            model_file=ML_CFG["model_file"],
            accuracy=float(test_accuracy),
            loss=float(test_loss),
            val_accuracy=float(history.history.get("val_accuracy", [0.0])[-1]),
            val_loss=float(history.history.get("val_loss", [0.0])[-1]),
            precision=macro["precision"],
            recall=macro["recall"],
            f1_score=macro["f1"],
            confusion_matrix=[[int(cm[0][0]), int(cm[0][1])], [int(cm[1][0]), int(cm[1][1])]],
            history={k: [round(float(x), 4) for x in v] for k, v in history.history.items()},
            per_class_metrics=per_class,
            notes=(
                "Automatically recorded on this training run. Active model: "
                "{0} ({1}).".format(ML_CFG["name"], ML_CFG["model_file"])
            ),
        )
        print("\nTraining metrics persisted to the application database.")
    except Exception as e:  # noqa: BLE001
        print("\nWarning: could not persist training metrics ({0}).".format(e))


_persist_training_metrics()

