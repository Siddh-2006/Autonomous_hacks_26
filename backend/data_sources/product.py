# Product data source
def get_product_signals():
    """Fetch product development signals"""
    # Placeholder implementation
    # In real implementation, would analyze release notes, changelogs, etc.
    return {
        "release_velocity": 0.4,  # Below threshold
        "features_released": 2,
        "bugs_fixed": 8,
        "user_feedback_score": 3.2,
        "community_activity": "declining"
    }

def get_user_sentiment():
    """Analyze user sentiment from forums, reviews"""
    return {
        "overall_sentiment": "mixed",
        "satisfaction_score": 3.1,
        "complaint_categories": ["performance", "bugs", "missing features"]
    }