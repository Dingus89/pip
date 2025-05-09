import sounddevice as sd
import numpy as np
import asyncio

THRESHOLD = 0.2  # Adjust for sensitivity (0–1 range)

async def detect_loud_sounds():
    def audio_callback(indata, frames, time, status):
        volume_norm = np.linalg.norm(indata) * 10
        if volume_norm > THRESHOLD:
            print(f"[Mic] Loud sound detected: {volume_norm:.2f}")

    print("[Mic] Starting loud sound detector...")
    with sd.InputStream(callback=audio_callback):
        while True:
            await asyncio.sleep(0.5)
