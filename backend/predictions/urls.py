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
]
