import random


class EmotionManager:
    def __init__(self):
        self.current_emotion = "neutral"

    def get_current_emotion(self):
        return self.current_emotion

    def update_emotion(self, user_input, response=None):
        if "thank" in user_input.lower():
            self.current_emotion = "happy"
        elif "angry" in user_input.lower():
            self.current_emotion = "concerned"
        elif "fun" in user_input.lower() or "joke" in user_input.lower():
            self.current_emotion = "excited"
        elif "lonely" in user_input.lower():
            self.current_emotion = "sad"
        else:
            self.current_emotion = random.choice([
                "curious", "friendly", "neutral"
            ])
