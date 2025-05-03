import random


class PipCuriosity:
    def __init__(self):
        self.questions = [
            "What’s your favorite sound?",
            "Do you think robots can dream?",
            "What’s something you wish you could learn instantly?",
            "What makes you smile?",
            "What do you think I'm good at?",
            "Is there something you wish I could do?",
        ]
        self.asked_today = []

    def get_question(self):
        remaining = [q for q in self.questions if q not in self.asked_today]
        if not remaining:
            self.asked_today = []
            remaining = self.questions.copy()
        q = random.choice(remaining)
        self.asked_today.append(q)
        return q
