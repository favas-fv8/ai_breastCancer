# ============================================================
# Breast Cancer Histology Image Classification using CNN
# CancerNet Model using TensorFlow / Keras
# ============================================================

# ============================================================
# 1. IMPORT LIBRARIES
# ============================================================

import os
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

IMG_SIZE = 50
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

model.save("CancerNet_Model.h5")

print("\nModel Saved Successfully")

