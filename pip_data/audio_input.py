import os
import queue
import sounddevice as sd
import vosk
import json
import serial
import time

def get_input_device():
    devices = sd.query_devices()
    for i, d in enumerate(devices):
        if "USB" in d['name'] and d['max_input_channels'] > 0:
            print(f"[Audio] Using USB microphone: {d['name']}")
            return i
    print("[Audio] USB mic not found, using ESP32 mic over UART")
    return None

def recognize_from_uart(timeout=8):
    try:
        uart = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
        uart.write(b'RECORD\n')  # Optional: if your ESP32 listens for this trigger
        data = b""
        start = time.time()
        while time.time() - start < timeout:
            if uart.in_waiting:
                data += uart.read(uart.in_waiting)
        return data.decode(errors="ignore").strip()
    except Exception as e:
        print(f"[Audio] UART mic error: {e}")
        return ""

def recognize_from_mic(timeout=8):
    model_path = "models/vosk-model-small-en-us-0.15"
    if not os.path.exists(model_path):
        print("[STT] Vosk model not found.")
        return ""

    device = get_input_device()
    if device is None:
        return recognize_from_uart(timeout)

    q = queue.Queue()
    model = vosk.Model(model_path)
    samplerate = 16000

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