from django.urls import path
from . import views

urlpatterns = [
    path('api/energy-valve-data/', views.EnergyValveDataAPIView.as_view()),
    path('api/hourly-heatmap/', views.HourlyHeatmapAPIView.as_view()),
    # Add more URL patterns for other visualizations
]