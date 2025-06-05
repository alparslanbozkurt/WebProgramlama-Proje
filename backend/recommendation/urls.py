from django.urls import path
from .views import AIPersonalizedRecommendationView

urlpatterns = [
    path("ai_recommendations/", AIPersonalizedRecommendationView.as_view()),
]
