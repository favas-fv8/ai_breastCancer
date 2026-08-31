from django.contrib import admin

from .models import Prediction


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "result", "confidence", "created_at"]
    list_filter = ["result", "created_at"]
    search_fields = ["user__username", "result"]
    readonly_fields = ["confidence", "probability", "created_at"]
