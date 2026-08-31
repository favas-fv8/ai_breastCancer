from django.db import models
from django.conf import settings


class Prediction(models.Model):
    """Stores a single histopathology image prediction performed by the user."""

    RESULT_CHOICES = [
        ("Benign", "Benign"),
        ("Malignant", "Malignant"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="predictions",
    )
    image = models.ImageField(upload_to="predictions/%Y/%m/%d/")
    result = models.CharField(max_length=20, choices=RESULT_CHOICES)
    confidence = models.FloatField(default=0.0, help_text="Confidence percentage (0-100).")
    probability = models.FloatField(default=0.0, help_text="Raw model probability (0-1).")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.user.username} - {self.result} ({self.confidence:.1f}%)"


class ModelTraining(models.Model):
    """Captures the performance metrics of a completed training run.

    A new record is created every time a model / dataset is (re)trained, so
    the latest record always reflects the most recent model performance
    (accuracy, loss, confusion matrix, per-class metrics, training history).
    """

    name = models.CharField(max_length=120, help_text="Model name, e.g. CancerNet.")
    version = models.CharField(max_length=60, help_text="Version tag of this training run.")
    dataset_name = models.CharField(max_length=120, default="IDC_regular_ps50_idx5")

    # Training configuration
    image_size = models.IntegerField(default=50)
    classes = models.IntegerField(default=2)
    epochs_total = models.IntegerField(default=0)
    epochs_run = models.IntegerField(default=0)
    batch_size = models.IntegerField(default=32)
    train_samples = models.IntegerField(default=0)
    val_samples = models.IntegerField(default=0)
    test_samples = models.IntegerField(default=0)
    model_file = models.CharField(max_length=255, default="CancerNet_Model.h5")

    # Global metrics
    accuracy = models.FloatField(default=0.0, help_text="Test accuracy (0-1).")
    loss = models.FloatField(default=0.0, help_text="Test loss.")
    val_accuracy = models.FloatField(default=0.0)
    val_loss = models.FloatField(default=0.0)

    # Classification report derived metrics (macro averages over classes)
    precision = models.FloatField(default=0.0)
    recall = models.FloatField(default=0.0)
    f1_score = models.FloatField(default=0.0)

    # Confusion matrix: [[true_neg, false_pos], [false_neg, true_pos]]
    # stored as a flat list or 2D list of cell counts.
    confusion_matrix = models.JSONField(default=list, blank=True)

    # Per-epoch training history for charts, e.g.
    # {"accuracy": [...], "loss": [...], "val_accuracy": [...], "val_loss": [...]}
    history = models.JSONField(default=dict, blank=True)

    # Per-class metrics, e.g.
    # [{"class": "Benign", "precision": .., "recall": .., "f1": .., "support": ..}]
    per_class_metrics = models.JSONField(default=list, blank=True)

    notes = models.TextField(blank=True, default="")
    trained_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-trained_at"]

    def __str__(self) -> str:
        return f"{self.name} v{self.version} - acc {self.accuracy:.2%}"

    @property
    def latest_accuracy(self) -> float:
        return self.accuracy  # convenience alias used by the API
