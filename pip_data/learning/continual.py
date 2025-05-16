import time
from learning.feedback import FeedbackClassifier
from learning.importance import ImportanceEstimator
from memory.vectors import VectorMemory  # If needed by base_model
from memory.cache import TokenCache      # Optional for context
from contextlib import suppress

class ContinualLearningAI:
    def __init__(self, base_model, memory_store, learning_rate=0.01):
        self.base_model = base_model
        self.memory_store = memory_store
        self.learning_rate = learning_rate
        self.confidence_threshold = 0.85

        self.privacy_filter = PrivacyFilter()
        self.feedback_classifier = FeedbackClassifier(base_model=base_model)
        self.importance_estimator = ImportanceEstimator()

    def process_user_interaction(self, user_input, context):
        response = self.base_model.generate(user_input, context)

        self.memory_store.add_interaction(
            user_input=user_input,
            context=context,
            model_response=response,
            timestamp=time.time(),
            session_id=context.session_id,
            is_private=False,
            is_learnable=True
        )

        self.privacy_filter.is_safe_to_learn(interaction)
        self.memory_store.store(interaction)

        return interaction

    def process_user_feedback(self, interaction_id, feedback_type, correction=None):
        interaction = self.memory_store.get_interaction(interaction_id)

        # Handle raw feedback dict
        if isinstance(feedback_type, dict):
            rating_score = self.feedback_classifier.classify_explicit_feedback(feedback_type)
            feedback_type = "positive" if rating_score > 0 else "negative"

        if feedback_type == "correction" and correction:
            self._learn_from_correction(interaction, correction)
        elif feedback_type in ["positive", "negative"]:
            self._update_confidence_scores(interaction, feedback_type)

        self.memory_store.add_feedback(interaction_id, feedback_type, correction)

    def background_learning_cycle(self):
        candidates = self.memory_store.get_valuable_learning_samples(self.importance_estimator)
        safe_samples = [s for s in candidates if self.privacy_filter.is_safe_to_learn(s)]

        if safe_samples:
            self.base_model.update_weights(
                safe_samples,
                learning_rate=self.learning_rate * 0.5
            )

    def _learn_from_correction(self, interaction, correction):
        training_sample = self._prepare_training_sample(interaction, correction)
        if self.privacy_filter.is_safe_to_learn(training_sample):
            self.base_model.update_weights(
                [training_sample],
                learning_rate=self.learning_rate
            )

    def _prepare_training_sample(self, interaction, correction=None):
        # Stub: define format as needed
        return {
            "input": interaction.user_input,
            "expected_output": correction,
            "context": interaction.context
        }

    def _update_confidence_scores(self, interaction, feedback_type):
        # Hook for future confidence tracking
        pass


class PrivacyFilter:
    def __init__(self):
        self.pii_detector = PIIDetector()

    def is_safe_to_learn(self, sample):
        if self.pii_detector.contains_pii(sample.user_input):
            sample.is_private = True
            sample.is_learnable = False
            return False
        sample.is_private = False
        sample.is_learnable = True
        return True


class PIIDetector:
    def contains_pii(self, text):
        patterns = [
            r"\b\d{3}-\d{2}-\d{4}\b",  # SSN
            r"\b\d{10}\b",            # Phone
            r"\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b",  # Email
            r"\b\d{1,3} \w+ (St|Ave|Blvd|Rd|Dr),? [A-Z]{2} \d{5}\b"  # Address
        ]
        return any(re.search(p, text) for p in patterns)
