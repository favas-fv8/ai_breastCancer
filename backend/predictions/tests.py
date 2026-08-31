from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient

from .models import ModelTraining, Prediction

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


class ModelTrainingApiTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="testpass12345")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.training = ModelTraining.objects.create(
            name="CancerNet",
            version="vTest-9",
            accuracy=0.80,
            loss=0.45,
            precision=0.78,
            recall=0.77,
            f1_score=0.77,
            confusion_matrix=[[80, 20], [10, 90]],
        )

    def test_list_models(self):
        resp = self.client.get("/api/models/")
        self.assertEqual(resp.status_code, 200)
        self.assertGreaterEqual(len(resp.data), 1)
        self.assertTrue(any(m["name"] == "CancerNet" for m in resp.data))

    def test_latest_model(self):
        resp = self.client.get("/api/models/latest/")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data["id"] == self.training.id)
        self.assertEqual(resp.data["accuracy_pct"], 80.0)

    def test_requires_auth(self):
        anon = APIClient()
        self.assertEqual(anon.get("/api/models/").status_code, 401)
