# CancerNet — Breast Cancer Histopathology CNN

This directory contains the original deep-learning training pipeline that
produced the `CancerNet_Model.h5` used by the web application.

## Files

- `cancer_detection.py` — standalone training/inference script.

## Pipeline overview

1. Loads all 50×50 histopathology image patches from `IDC_regular_ps50_idx5`.
2. Labels: `0` = **IDC_negative** (Benign), `1` = **IDC_positive** (Malignant).
3. Splits into train / validation / test (stratified).
4. Preprocesses with `ImageDataGenerator` (rescale to `[0,1]`, augmentation).
5. Builds a sequential CNN (`32 → 64 → 128` conv filters + dropout + sigmoid).
6. Trains with Adam, binary cross-entropy and early stopping.
7. Evaluates and saves the model as `CancerNet_Model.h5`.

## Re-training

```bash
python cancer_detection.py
```

The dataset folder must be present at the project root (`IDC_regular_ps50_idx5/`)
for the script to load data.

After training completes, the script automatically records a
`ModelTraining` entry (accuracy, loss, confusion matrix, per-class metrics and
training history) into the web application's PostgreSQL database. The frontend
**Model Performance** page reads this record, so it updates automatically on
every training run. If the Django environment/database is unavailable, the
training still completes — it simply skips the metrics persistence step.
