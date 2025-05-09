import cv2
import asyncio

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

async def detect_faces():
    cap = cv2.VideoCapture(0)  # Use first connected webcam
    if not cap.isOpened():
        print("[Camera] Failed to open webcam.")
        return

    print("[Camera] Webcam started for face detection.")
    while True:
        ret, frame = cap.read()
        if not ret:
            await asyncio.sleep(1)
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        if len(faces) > 0:
            print(f"[Camera] Detected {len(faces)} face(s)")

        await asyncio.sleep(1)  # Prevent excessive CPU usage
