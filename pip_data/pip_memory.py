import json
import os


class MemoryManager:
    def __init__(self, memory_file="pip_ai_server/data/memory.json"):
        self.memory_file = memory_file
        self.memory_data = self.load_memory()

    def load_memory(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, "r") as f:
                return json.load(f)
        return {}

    def store_interaction(self, user_input, response):
        self.memory_data[user_input] = response
        os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
        with open(self.memory_file, "w") as f:
            json.dump(self.memory_data, f, indent=2)

    def recall_response(self, user_input):
        return self.memory_data.get(user_input)
