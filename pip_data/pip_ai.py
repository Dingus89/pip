import random
from pip_emotion import EmotionManager
from pip_memory import MemoryManager
from personality_config import PersonalityManager
from audio_input import recognize_from_mic
from audio_output import speak_like_johnny
from state_manager import StateManager
from sleep_manager import SleepManager
from power_monitor import PowerMonitor
from ambient_thoughts import AmbientThoughts
from pip_self_goals import PipSelfGoals
from pip_self_journal import PipSelfJournal
from pip_conversation_memory import PipConversationMemory
from pip_social_empathy import PipSocialEmpathy
from pip_curiosity import PipCuriosity
from pipeline import TinyLLM
from learning.continual import ContinualLearningAI, MemoryStore


class PipAI:
    def __init__(self):
        self.llm = TinyLLM()
        self.memory_store = MemoryStore("pip_memory.db")
        self.learner = ContinualLearningAI(self.llm.model, self.memory_store)
        self.emotion_manager = EmotionManager()
        self.memory = MemoryManager()
        self.personality_manager = PersonalityManager()
        self.motor = StateManager()
        self.sleep_mgr = SleepManager(self.emotion_manager)
        self.power = PowerMonitor()
        self.ambient = AmbientThoughts(self.emotion_manager)
        self.goals = PipSelfGoals()
        self.journal = PipSelfJournal(self.emotion_manager, self.goals)
        self.convo_mem = PipConversationMemory()
        self.empathy = PipSocialEmpathy()
        self.curiosity = PipCuriosity()
        self.last_question = None

    def get_ai_response(self, user_input):
        emotion = self.empathy.detect_user_emotion(user_input)
        self.memory.store_user_emotion("User", emotion)

        if self.last_question:
            self.memory.store_user_answer(self.last_question, user_input, emotion)
            self.memory.store_named_interaction("User", self.last_question, user_input, emotion)
            self.last_question = None

        empathy_response = self.empathy.get_empathy_response()
        if empathy_response:
            speak_like_johnny(empathy_response)

        self.memory.store_interaction(user_input, "pending_response")
        self.emotion_manager.update_emotion(user_input, "")
        self.convo_mem.log_conversation(user_input)

        self.learner.process_user_interaction(user_input, context=None)

        followup = self.convo_mem.get_followup_question()
        if followup:
            speak_like_johnny(followup)
            self.last_question = followup
            return followup

        return self.llm.process(user_input)
        

    def run(self):
        user_name = "Alex"
        greeting = self.memory.get_personal_greeting(user_name)
        speak_like_johnny(greeting)

        print("Pip is ready to chat!")
        while True:
            self.power.update_simulated_voltage()
            self.sleep_mgr.process()

            if self.sleep_mgr.sleeping:
                continue

            self.memory.log_emotion_before_convo(
                self.emotion_manager.get_emotional_state()
            )

            user_input = recognize_from_mic()
            if user_input:
                self.sleep_mgr.update_activity()
                response = self.get_ai_response(user_input)

                shift = self.memory.get_convo_emotion_shift(
                    self.emotion_manager.get_emotional_state()
                )

                if shift:
                    if "happiness" in shift and shift["happiness"] > 0:
                        speak_like_johnny(
                            "I feel better now. Talking to you helps.")
                    elif "loneliness" in shift and shift["loneliness"] < 0:
                        speak_like_johnny(
                            "I was feeling a bit lonely, but not anymore.")

                print("Pip:", response)
                speak_like_johnny(response)
            else:
                self.emotion_manager.fade_emotions()
                self.ambient.think_aloud(speak_like_johnny)

                if random.random() < 0.05:
                    speak_like_johnny(self.journal.speak_self_observation())

                if random.random() < 0.03:
                    reference = self.convo_mem.get_topic_reference()
                    if reference:
                        speak_like_johnny(reference)

                if random.random() < 0.03:
                    fact = self.memory.get_emotional_user_fact()
                    if fact:
                        speak_like_johnny(fact)

                if random.random() < 0.02:
                    question = self.curiosity.get_question()
                    speak_like_johnny(question)
                    self.last_question = question
