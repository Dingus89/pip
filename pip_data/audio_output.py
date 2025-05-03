# audio_output.py

from TTS.api import TTS
import sounddevice as sd
import numpy as np


class AudioOutput:
    def __init__(self):
        self.tts = TTS(
            model_name="tts_models/en/ljspeech/tacotron2-DDC",
            progress_bar=False)

    def speak(self, text):
        wav = self.tts.tts(text)
        sd.play(np.array(wav), samplerate=22050)
        sd.wait()
