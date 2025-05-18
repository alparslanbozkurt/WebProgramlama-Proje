from recommendation.strategies.content_based import ContentBasedRecommendation

def get_recommendations_for_user(user):
    strategy = ContentBasedRecommendation()
    return strategy.recommend(user)
