import subprocess
import os

AUDIO_PATH = "/home/aml/pip_data/audio"

def speak(text):
    print(f"[TTS] Speaking: {text}")
    if not os.path.exists(AUDIO_PATH):
        os.makedirs(AUDIO_PATH)

    wav_file = os.path.join(AUDIO_PATH, "speech.wav")
    cmd = [
        "tts",
        "--text", text,
        "--model_name", "tts_models/en/jenny/jenny",
        "--speaker_idx", "p231",
        "--out_path", wav_file
    ]
    subprocess.run(cmd)

    subprocess.run(["aplay", wav_file])

