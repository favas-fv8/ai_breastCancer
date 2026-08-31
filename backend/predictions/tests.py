from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from .models import Prediction

User = get_user_model()


class PredictionModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="testpass12345")

    def test_create_prediction(self):
        img = SimpleUploadedFile("sample.png", b"fake-image-bytes", content_type="image/png")
        pred = Prediction.objects.create(
            user=self.user,
            image=img,
            result="Benign",
            confidence=88.5,
            probability=0.115,
        )
        self.assertEqual(pred.result, "Benign")
        self.assertEqual(pred.confidence, 88.5)
        self.assertEqual(str(pred.user.username), "tester")
