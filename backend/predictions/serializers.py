from rest_framework import serializers

from .models import ModelTraining, Prediction


class PredictionSerializer(serializers.ModelSerializer):
    """Serializes a completed prediction for list/retrieve/delete operations."""

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Prediction
        fields = ["id", "image", "result", "confidence", "probability", "created_at"]


class PredictionCreateSerializer(serializers.Serializer):
    """Validates the uploaded image file before running inference."""

    image = serializers.ImageField(required=True)

    def validate_image(self, value):
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("Image size must not exceed 5 MB.")
        return value


class ModelTrainingSerializer(serializers.ModelSerializer):
    """Serializes a training run plus chart-friendly derived fields."""

    trained_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    accuracy_pct = serializers.SerializerMethodField()
    precision_pct = serializers.SerializerMethodField()
    recall_pct = serializers.SerializerMethodField()
    f1_pct = serializers.SerializerMethodField()
    class_labels = serializers.SerializerMethodField()

    class Meta:
        model = ModelTraining
        fields = [
            "id",
            "name",
            "version",
            "dataset_name",
            "image_size",
            "classes",
            "epochs_total",
            "epochs_run",
            "batch_size",
            "train_samples",
            "val_samples",
            "test_samples",
            "model_file",
            "accuracy",
            "accuracy_pct",
            "loss",
            "val_accuracy",
            "val_loss",
            "precision",
            "precision_pct",
            "recall",
            "recall_pct",
            "f1_score",
            "f1_pct",
            "confusion_matrix",
            "history",
            "per_class_metrics",
            "class_labels",
            "notes",
            "trained_at",
        ]

    def _pct(self, value: float) -> float:
        try:
            return round(float(value) * 100, 2)
        except (TypeError, ValueError):
            return 0.0

    def get_accuracy_pct(self, obj):
        return self._pct(obj.accuracy)

    def get_precision_pct(self, obj):
        return self._pct(obj.precision)

    def get_recall_pct(self, obj):
        return self._pct(obj.recall)

    def get_f1_pct(self, obj):
        return self._pct(obj.f1_score)

    def get_class_labels(self, obj):
        labels = []
        for item in obj.per_class_metrics or []:
            labels.append(item.get("class", ""))
        if not labels:
            labels = [f"Class {i}" for i in range(obj.classes or 2)]
        return labels
