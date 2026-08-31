from django.urls import path

from . import views

urlpatterns = [
    path("predict/", views.predict_view, name="predict"),
    path("history/", views.PredictionListView.as_view(), name="history-list"),
    path(
        "history/<int:pk>/",
        views.PredictionDetailView.as_view(),
        name="history-detail",
    ),
    # Model training / performance
    path("models/", views.ModelTrainingListView.as_view(), name="model-list"),
    path("models/latest/", views.model_training_latest_view, name="model-latest"),
    path(
        "models/<int:pk>/",
        views.ModelTrainingDetailView.as_view(),
        name="model-detail",
    ),
]
