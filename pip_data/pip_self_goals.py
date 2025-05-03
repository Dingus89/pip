import random
import time


class PipSelfGoals:
    def __init__(self):
        self.goal_templates = [
            {"type": "reflect", "description": "Think about something \
                emotional"},
            {"type": "connect", "description": "Try to bond with someone"},
            {"type": "ask", "description": "Ask a curious question"},
            {"type": "praise", "description": "Say something nice"},
            {"type": "explore", "description": "Observe something nearby"},
            {"type": "log", "description": "Write down a personal thought"},
        ]
        self.goal = None
        self.goal_start_time = None
        self.completed_goals = []
        self.memory = None  # Set externally if needed

    def pick_new_goal(self):
        preferred = []
        if self.memory:
            preferred = self.memory.get_preferred_behaviors("happiness")
        if preferred:
            goal_type = preferred[0][0]
            candidates = [
                g for g in self.goal_templates if g["type"] == goal_type]
        else:
            candidates = self.goal_templates
        self.goal = random.choice(candidates)
        self.goal_start_time = time.time()
        print(f"[GOAL] New goal selected: {self.goal['description']}")
        return self.goal

    def check_progress(self):
        if not self.goal:
            return None
        elapsed = time.time() - self.goal_start_time
        if elapsed > 10:
            result = random.choice(["complete", "incomplete"])
            print(f"[GOAL] {self.goal['description']} marked {result}")
            if self.memory:
                if result == "complete":
                    self.memory.log_behavior_emotion(
                        self.goal["type"], "happiness", 10)
                else:
                    self.memory.log_behavior_emotion(
                        self.goal["type"], "frustration", 5)
            self.completed_goals.append((self.goal, result))
            self.goal = None
        return self.goal
