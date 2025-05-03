# ambient_thoughts.py

import random
import time
from pip_reflection import PipReflection
from pip_dreams import PipDreams


class AmbientThoughts:
    def __init__(self, emotion_engine):
        self.last_spoken = time.time()
        self.cooldown = 90  # seconds between idle thoughts
        self.reflection = PipReflection(emotion_engine)
        self.dreams = PipDreams()

    def should_think_aloud(self):
        if (time.time() - self.last_spoken) >= self.cooldown:
            return random.random() < 0.3  # 30% chance to speak
        return False

    def generate_thought(self):
        if random.random() < 0.5:
            return self.reflection.generate_thought()
        else:
            return self.dreams.get_dream()

    def think_aloud(self, speak_func):
        if self.should_think_aloud():
            thought = self.generate_thought()
            if thought:
                speak_func(thought)
                self.last_spoken = time.time()
