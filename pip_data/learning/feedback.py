class FeedbackClassifier:
    def __init__(self, base_model):
        self.base_model = base_model
        self.explicit_feedback_classifier = DummyClassifier()
        self.implicit_feedback_classifier = DummyClassifier()

    def classify_explicit_feedback(self, feedback_data):
        if "rating" in feedback_data:
            return self._normalize_rating(feedback_data["rating"])
        if "feedback_text" in feedback_data:
            return self.explicit_feedback_classifier.predict(feedback_data["feedback_text"])
        return 0.0

    def classify_implicit_feedback(self, interaction):
        signals = []

        if getattr(interaction, "followed_by_further_interaction", False):
            signals.append(("continued_engagement", 0.6))
        if getattr(interaction, "followed_by_reformulation", False):
            signals.append(("reformulation", -0.4))
        if getattr(interaction, "resulted_in_session_abandonment", False):
            signals.append(("abandonment", -0.5))
        if getattr(interaction, "recommendation_acted_upon", False):
            signals.append(("recommendation_usage", 0.8))

        if signals:
            return max(-1.0, min(1.0, sum(w for _, w in signals) / len(signals)))
        return 0.0

    def _normalize_rating(self, rating):
        return (rating - 3) / 2.0 if isinstance(rating, (int, float)) else 0.0


class DummyClassifier:
    def predict(self, text):
        text = text.lower()
        if "good" in text:
            return 1.0
        if "bad" in text:
            return -1.0
        return 0.0
