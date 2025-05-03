class PersonalityManager:
    def __init__(self):
        self.personality = {
            "tone": "friendly",
            "energy": "high",
            "interests": ["learning", "exploring", "helping"]
        }

    def get_personality(self):
        return self.personality

    def set_personality(self, personality_dict):
        self.personality = personality_dict
