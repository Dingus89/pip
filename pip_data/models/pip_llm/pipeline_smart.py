from pipeline import TinyLLM
from learning.continual import ContinualLearningAI, MemoryStore
from types import SimpleNamespace
import time


class SmartPip:
    def __init__(self):
        self.llm = TinyLLM()
        self.memory_store = MemoryStore(database_connection="pip_memory.db")
        self.learner = ContinualLearningAI(
            base_model=self.llm.model,
            memory_store=self.memory_store
        )

    def chat(self, user_input):
        context = self._build_context()
        response = self.llm.process(user_input)

        self.learner.process_user_interaction(
            user_input=user_input,
            context=context
        )

        return response

    def give_feedback(self, interaction_id, feedback_type, correction=None):
        self.learner.process_user_feedback(interaction_id, feedback_type, correction)

    def retrain_if_needed(self):
        """Manual or scheduled trigger"""
        self.learner.background_learning_cycle()

    def _build_context(self):
        return SimpleNamespace(
            session_id="local-session",
            timestamp=time.time()
        )
