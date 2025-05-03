class PipSocialEmpathy:
    def __init__(self):
        self.last_user_emotion = "neutral"

    def detect_user_emotion(self, user_input):
        text = user_input.lower()
        if "tired" in text or "exhausted" in text:
            self.last_user_emotion = "tired"
        elif "happy" in text or "awesome" in text:
            self.last_user_emotion = "happy"
        elif "sad" in text or "lonely" in text:
            self.last_user_emotion = "sad"
        elif "mad" in text or "angry" in text:
            self.last_user_emotion = "angry"
        else:
            self.last_user_emotion = "neutral"
        return self.last_user_emotion

    def get_empathy_response(self):
        em = self.last_user_emotion
        if em == "tired":
            return "You should take it easy. I’ll be here when you need me."
        elif em == "happy":
            return "Yay! I'm happy you're happy!"
        elif em == "sad":
            return "I’m sorry you're feeling down. I’m here for you."
        elif em == "angry":
            return "That sounds frustrating. Want to talk about it?"
        return None
