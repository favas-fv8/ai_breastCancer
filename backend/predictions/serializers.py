from rest_framework import serializers

from .models import Prediction


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
