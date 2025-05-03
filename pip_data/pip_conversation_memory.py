import json
import os
import re
import random

CONVO_LOG = "conversation_topics.json"


class PipConversationMemory:
    def __init__(self):
        self.topics = {}
        self.load()

    def load(self):
        if os.path.exists(CONVO_LOG):
            with open(CONVO_LOG, "r") as f:
                self.topics = json.load(f)
        else:
            self.topics = {}

    def save(self):
        with open(CONVO_LOG, "w") as f:
            json.dump(self.topics, f, indent=2)

    def extract_keywords(self, text):
        words = re.findall(r'\b\w+\b', text.lower())
        ignore = {
            "the", "and", "you", "are", "what", "is",
            "how", "can", "a", "i", "me", "my"
        }
        return [w for w in words if len(w) > 3 and w not in ignore]

    def log_conversation(self, text):
        for word in self.extract_keywords(text):
            self.topics[word] = self.topics.get(word, 0) + 1
        self.save()

    def get_top_topics(self, n=3):
        sorted_topics = sorted(
            self.topics.items(),
            key=lambda x: x[1],
            reverse=True)
        return [word for word, _ in sorted_topics[:n]]

    def get_topic_reference(self):
        top = self.get_top_topics()
        if not top:
            return None
        return f"You talk a lot about {', '.join(top)}. I like learning what \
            matters to you!"

    def get_followup_question(self):
        top = self.get_top_topics()
        if not top:
            return None
        topic = random.choice(top)
        prompts = [
            f"You've mentioned {topic} — what's your favorite thing about it?",
            f"Should we talk more about {topic} sometime?",
            f"What do you love about {topic}?"
        ]
        return random.choice(prompts)

    def get_suggestion(self):
        top = self.get_top_topics()
        if not top:
            return None
        topic = random.choice(top)
        return f"If you're bored, we could chat more \
            about {topic} — you seem to enjoy it!"
