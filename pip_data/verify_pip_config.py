import os
import json
from pip_config import (
    MEMORY_JSON,
    JOURNAL_TXT,
    VOSK_MODEL,
    Tinyllm,
    COQUI_MODEL_DIR,
    AUDIO_TMP
)


def check_create_file(path, default=None):
    if os.path.exists(path):
        return "✅ Found"
    with open(path, "w") as f:
        if default is not None:
            json.dump(default, f, indent=2)
    return "➕ Created"


def check_create_dir(path):
    if os.path.isdir(path):
        return "✅ Found"
    os.makedirs(path, exist_ok=True)
    return "➕ Created"


def main():
    print("Verifying Pip system files and directories...\n")

    memory_default = {
        "names": [],
        "favorites": {
            "sound": None,
            "song": None,
            "word": None,
            "place": None
        },
        "emotional_log": [],
        "journal_count": 0,
        "first_boot": None
    }

    print("MEMORY_JSON:", MEMORY_JSON, "→",
          check_create_file(MEMORY_JSON, default=memory_default))
    print("JOURNAL_TXT:", JOURNAL_TXT, "→",
          check_create_file(JOURNAL_TXT))
    print("VOSK_MODEL:", VOSK_MODEL, "→",
          check_create_dir(VOSK_MODEL))
    print("TINY_LLAMA_MODEL:", TINY_LLAMA_MODEL, "→",
          "✅ Found" if os.path.exists(TINY_LLAMA_MODEL) else "❌ Missing")
    print("COQUI_MODEL_DIR:", COQUI_MODEL_DIR, "→",
          check_create_dir(COQUI_MODEL_DIR))
    print("AUDIO_TMP:", AUDIO_TMP, "→",
          check_create_dir(AUDIO_TMP))

    print("\n✅ Setup complete. All paths verified or created.")
    if not os.path.exists(TINY_LLAMA_MODEL):
        print("⚠️ TinyLlama model is missing — transfer it manually.")


if __name__ == "__main__":
    main()
