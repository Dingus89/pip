import math

class ImportanceEstimator:
    def __init__(self):
        self.importance_classifier = DummyImportanceClassifier()
        self.concept_tracker = ConceptTracker()

    def estimate_importance(self, interaction):
        features = self._extract_importance_features(interaction)
        base = self.importance_classifier.predict(features)

        adjustments = [
            self._calculate_novelty_score(interaction) * 0.3,
            self._calculate_error_correction_value(interaction) * 0.4,
            self._calculate_conceptual_gap_score(interaction) * 0.25,
            self._calculate_user_emphasis(interaction) * 0.2
        ]

        return max(0.0, min(1.0, base + sum(adjustments)))

    def _extract_importance_features(self, interaction):
        return {"text": interaction.user_input, "context": interaction.context}

    def _calculate_novelty_score(self, interaction):
        concepts = self.concept_tracker.extract_concepts(interaction.user_input)
        if not concepts: return 0
        return sum(self.concept_tracker.get_concept_rarity(c) for c in concepts) / len(concepts)

    def _calculate_error_correction_value(self, interaction):
        return 0.5 + 0.5 * getattr(interaction, "original_confidence", 0.0) if getattr(interaction, "is_correction", False) else 0.0

    def _calculate_conceptual_gap_score(self, interaction):
        return 0.1  # Placeholder

    def _calculate_user_emphasis(self, interaction):
        signals = ["important", "remember this", "crucial", "take note"]
        text = interaction.user_input.lower()
        return 0.8 if any(s in text for s in signals) else 0.0


class DummyImportanceClassifier:
    def predict(self, features):
        return 0.3 if "remember" in features.get("text", "").lower() else 0.1


class ConceptTracker:
    def __init__(self):
        self.concepts = {}

    def extract_concepts(self, text):
        return [w for w in text.lower().split() if len(w) > 4]

    def get_concept_rarity(self, concept):
        count = self.concepts.get(concept, 0)
        self.concepts[concept] = count + 1
        return 1.0 if count == 0 else 1.0 / (1.0 + math.log(self.concepts[concept]))
