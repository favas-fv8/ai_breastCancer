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
