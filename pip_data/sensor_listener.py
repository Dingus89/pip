import asyncio
from vision.camera_handler import detect_faces
from vision.mic_handler import detect_loud_sounds


class SensorListener:
    def __init__(self):
        pass

    async def start(self):
        asyncio.create_task(detect_faces())
        asyncio.create_task(detect_loud_sounds())
