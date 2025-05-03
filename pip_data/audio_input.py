import os
import queue
import sounddevice as sd
import vosk
import json


def recognize_from_mic(timeout=8):
    model_path = "models/vosk-model-small-en-us-0.15"
    if not os.path.exists(model_path):
        print("[STT] Vosk model not found.")
        return ""

    q = queue.Queue()
    model = vosk.Model(model_path)
    samplerate = 16000
    device = None  # Default input

    def callback(indata, frames, time_, status):
        if status:
            print(status)
        q.put(bytes(indata))

    with sd.RawInputStream(
        samplerate=samplerate,
        blocksize=8000,
        device=device,
        dtype="int16",
        channels=1,
        callback=callback
    ):
        rec = vosk.KaldiRecognizer(model, samplerate)
        print("[STT] Listening...")

        result_text = ""
        seconds = 0

        while seconds < timeout:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                result_text = result.get("text", "")
                break
            seconds += 0.5

        if not result_text:
            partial = json.loads(rec.PartialResult())
            result_text = partial.get("partial", "")

        print("[STT] Result:", result_text)
        return result_text.strip()
