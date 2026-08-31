from PIL import Image, UnidentifiedImageError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView, RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ml import predictor

from .models import Prediction
from .serializers import PredictionCreateSerializer, PredictionSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def predict_view(request):
    """Upload an image, run the deep learning model and store the result."""
    serializer = PredictionCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    upload = serializer.validated_data["image"]

    try:
        image = Image.open(upload)
        image.load()
    except (UnidentifiedImageError, OSError):
        return Response(
            {"image": "The uploaded file is not a valid image."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        result = predictor.predict(image)
    except Exception as exc:  # noqa: BLE001 - surface a friendly error to the user
        return Response(
            {"detail": f"Model prediction failed: {exc}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    prediction = Prediction.objects.create(
        user=request.user,
        image=upload,
        result=result["prediction"],
        confidence=result["confidence"],
        probability=result["probability"],
    )

    return Response(
        PredictionSerializer(prediction).data,
        status=status.HTTP_201_CREATED,
    )


class PredictionListView(ListAPIView):
    """Returns the authenticated user's prediction history (newest first)."""

    serializer_class = PredictionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Prediction.objects.filter(user=self.request.user)


class PredictionDetailView(RetrieveDestroyAPIView):
    """Retrieve or delete a specific history record (must own it)."""

    serializer_class = PredictionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Prediction.objects.filter(user=self.request.user)
