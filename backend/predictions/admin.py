from django.contrib import admin

from .models import ModelTraining, Prediction


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "result", "confidence", "created_at"]
    list_filter = ["result", "created_at"]
    search_fields = ["user__username", "result"]
    readonly_fields = ["confidence", "probability", "created_at"]


@admin.register(ModelTraining)
class ModelTrainingAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "version",
        "accuracy",
        "loss",
        "precision",
        "recall",
        "f1_score",
        "epochs_run",
        "trained_at",
    ]
    list_filter = ["name", "dataset_name", "trained_at"]
    search_fields = ["name", "version", "dataset_name"]
    readonly_fields = ["trained_at"]
