import json
import os
import datetime
import random


class PipMemoryCore:
    def __init__(self, memory_file="pip_data/pip_memory.json"):
        self.memory_file = memory_file
        self.memory = self.load()

    def load(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, "r") as f:
                return json.load(f)
        return {
            "people": {},
            "user_answers": {},
            "pip_preferences": {},
            "last_convo_emotion": {},
        }

    def save(self):
        with open(self.memory_file, "w") as f:
            json.dump(self.memory, f, indent=2)

    def store_user_answer(self, question, answer, emotion=None):
        self.memory.setdefault("user_answers", {})
        self.memory["user_answers"][question] = {
            "answer": answer,
            "timestamp": datetime.datetime.now().isoformat(),
            "emotion": emotion or "neutral"
        }
        self.save()

    def get_user_answer(self, question):
        return self.memory.get(
            "user_answers", {}).get(question, {}).get("answer")

    def get_emotional_user_fact(self):
        facts = self.memory.get("user_answers", {})
        emotional_facts = [
            f for f in facts.items()
            if f[1].get("emotion") in ("happiness", "lonely", "curious")
        ]
        if not emotional_facts:
            return None
        q, data = random.choice(emotional_facts)
        em = data["emotion"]
        if em == "happiness":
            return f'You told me "{data["answer"]}" and it made me feel happy.'
        elif em == "lonely":
            return f'I remember when you said "{data["answer"]}" — it helped \
                me feel less alone.'
        elif em == "curious":
            return f'Your answer "{data["answer"]}" made me think a lot.'
        return None

    def store_named_interaction(self, name, question, answer, emotion=None):
        self.memory.setdefault("people", {})
        person = self.memory["people"].setdefault(
            name, {"answers": {}, "moods": {}, "last_seen": None}
        )
        person["answers"][question] = {
            "answer": answer,
            "timestamp": datetime.datetime.now().isoformat(),
            "emotion": emotion or "neutral"
        }
        mood = person["moods"].get(emotion, 0)
        person["moods"][emotion] = mood + 1
        person["last_seen"] = datetime.datetime.now().isoformat()
        self.save()

    def get_person_summary(self, name):
        person = self.memory.get("people", {}).get(name)
        if not person:
            return f"Hi {name}! I'm happy to meet you."
        top_emotion = max(
            person["moods"], key=person["moods"].get, default="neutral")
        favs = [f"{q}: {a['answer']}" for q, a in person["answers"].items()]
        if not favs:
            return f"Hey {name}, you seem to feel mostly {top_emotion}."
        return f"{name} usually feels {top_emotion}. \
            I remember you said: {random.choice(favs)}"

    def get_personal_greeting(self, name):
        person = self.memory.get("people", {}).get(name)
        if not person:
            return f"Hi {name}! It's nice to meet you."
        top_emotion = max(
            person["moods"], key=person["moods"].get, default="neutral")
        mood_line = {
            "happy": "You usually seem happy when we talk!",
            "sad": "You've had some hard days, but I'm here for you.",
            "angry": "You've had strong feelings lately — I respect that.",
            "neutral": "It's always good connecting with you."
        }.get(top_emotion, "It's always good connecting with you.")
        return f"Hey {name}! {mood_line}"

    def log_behavior_emotion(self, behavior, emotion, value):
        prefs = self.memory.setdefault("pip_preferences", {})
        prefs.setdefault(behavior, {})
        prefs[behavior][emotion] = prefs[behavior].get(emotion, 0) + value
        self.save()

    def get_preferred_behaviors(self, target_emotion="happiness"):
        prefs = self.memory.get("pip_preferences", {})
        scored = [(b, v.get(target_emotion, 0)) for b, v in prefs.items()]
        return sorted(scored, key=lambda x: x[1], reverse=True)

    def log_emotion_before_convo(self, state):
        self.memory["last_convo_emotion"] = state
        self.save()

    def get_convo_emotion_shift(self, current_state):
        prev = self.memory.get("last_convo_emotion", {})
        change = {}
        for key in current_state:
            delta = current_state[key] - prev.get(key, 0)
            if abs(delta) >= 10:
                change[key] = delta
        return change if change else None
