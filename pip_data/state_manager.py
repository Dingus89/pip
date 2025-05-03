import random


class StateManager:
    def __init__(self):
        self.emotion_to_motion = {
            "happiness": self.spin_in_circles,
            "loneliness": self.wiggle,
            "curious": self.turn_left,
            "sad": self.stop,
            "angry": self.stomp,
        }

    def spin_in_circles(self):
        print("[Motion] Spinning in circles")

    def wiggle(self):
        print("[Motion] Wiggling in place")

    def turn_left(self):
        print("[Motion] Turning left slowly")

    def stop(self):
        print("[Motion] Stopping motion")

    def stomp(self):
        print("[Motion] Stomping or rapid tap")

    def perform_motion_by_emotion(self, emotion):
        motion = self.emotion_to_motion.get(emotion)
        if motion:
            print(f"[Motion] Triggered by emotion: {emotion}")
            motion()
        else:
            print(f"[Motion] No motion linked to emotion: {emotion}")

    def simulate_idle_motion(self):
        motion = random.choice(list(self.emotion_to_motion.values()))
        motion()
