import os

# Base directory (relative to current folder)
BASE = os.path.dirname(os.path.abspath(__file__))

MEMORY_JSON = os.path.join(BASE, "pip_data", "pip_memory.json")
JOURNAL_TXT = os.path.join(BASE, "pip_data", "pip_journal.txt")

VOSK_MODEL = os.path.join(BASE, "models", "vosk-model-small-en-us-0.15")
TINY_LLAMA_MODEL = os.path.join(
    BASE,
    "models",
    "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
)
COQUI_MODEL_DIR = os.path.join(BASE, "models", "coqui-tts-model-directory")

AUDIO_TMP = os.path.join(BASE, "tmp_audio")
