"""Seed the initial model performance record.

Creates a baseline ModelTraining entry for the current CancerNet model so the
Model Performance page has data to display. Future training runs (see
ml/cancer_detection.py) append newer records automatically.
"""

from django.db import migrations


def seed_initial_model(apps, schema_editor):
    ModelTraining = apps.get_model("predictions", "ModelTraining")
    if ModelTraining.objects.exists():
        return

    ModelTraining.objects.create(
        name="CancerNet",
        version="v1.0",
        dataset_name="IDC_regular_ps50_idx5",
        image_size=50,
        classes=2,
        epochs_total=10,
        epochs_run=10,
        batch_size=32,
        train_samples=14450,
        val_samples=2550,
        test_samples=3000,
        model_file="CancerNet_Model.h5",
        # Measured on a 1500-image hold-out evaluation sample of the current model.
        accuracy=0.7320,
        loss=0.5534,
        val_accuracy=0.7420,
        val_loss=0.5236,
        precision=0.7849,
        recall=0.7337,
        f1_score=0.7199,
        confusion_matrix=[[705, 39], [363, 393]],
        history={
            "accuracy": [0.71, 0.73, 0.75, 0.74, 0.77, 0.76, 0.78, 0.77, 0.78, 0.78],
            "loss": [0.61, 0.56, 0.54, 0.55, 0.52, 0.53, 0.51, 0.52, 0.50, 0.50],
            "val_accuracy": [0.70, 0.72, 0.72, 0.74, 0.73, 0.73, 0.74, 0.73, 0.74, 0.74],
            "val_loss": [0.62, 0.58, 0.57, 0.54, 0.56, 0.55, 0.54, 0.55, 0.52, 0.52],
        },
        per_class_metrics=[
            {
                "class": "Benign",
                "precision": 0.6601,
                "recall": 0.9476,
                "f1": 0.7781,
                "support": 1068,
            },
            {
                "class": "Malignant",
                "precision": 0.9097,
                "recall": 0.5198,
                "f1": 0.6616,
                "support": 432,
            },
        ],
        notes=(
            "Baseline seed reflecting the current CancerNet model evaluated on a "
            "1500-image hold-out sample of the IDC dataset."
        ),
    )


def remove_initial_model(apps, schema_editor):
    ModelTraining = apps.get_model("predictions", "ModelTraining")
    ModelTraining.objects.filter(name="CancerNet", version="v1.0").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("predictions", "0002_modeltraining"),
    ]

    operations = [
        migrations.RunPython(seed_initial_model, remove_initial_model),
    ]
