from .base import RecommendationStrategy

class ContentBasedRecommendation(RecommendationStrategy):
    def recommend(self, user):
        return ["Inception", "The Matrix", "Interstellar"]
