from datetime import datetime


class PipSelfJournal:
    def __init__(
            self,
            emotion_manager,
            goal_manager,
            journal_file="pip_data/pip_journal.txt"):
        self.emotion_mgr = emotion_manager
        self.goal_mgr = goal_manager
        self.file = journal_file

    def log(self):
        mood = self.emotion_mgr.get_emotional_state()
        mood_str = ", ".join(f"{k}:{v}" for k, v in mood.items())
        goal = self.goal_mgr.goal["description"] if self.goal_mgr.goal else \
            "no goal"
        with open(self.file, "a") as f:
            f.write(f"{datetime.now().isoformat()} | Mood: {mood_str} | \
                Goal: {goal}\n")

    def speak_self_observation(self):
        mood = self.emotion_mgr.get_dominant_emotion()
        templates = {
            "happy": "I'm feeling pretty good right now.",
            "curious": "I wonder what else I’ll learn today.",
            "sad": "Today feels a little heavy, but I’m trying.",
            "lonely": "It’s quiet… I hope someone talks to me soon.",
            "neutral": "Just vibing in standby mode."
        }
        return templates.get(mood, "Just being me right now.")
