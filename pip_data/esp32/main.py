# main.py

import network
import socket
import time
import ujson
import _thread

from esp32_motor_ir import send_ir_command
from sensor_handlers import read_pir, read_ultrasonic
from capacitance_sensor import read_touch

WIFI_SSID = "2c7b65"
WIFI_PASS = "rating.163.prevail"
PORT = 8266


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASS)
        while not wlan.isconnected():
            pass
    print("Connected:", wlan.ifconfig())


def websocket_server():
    s = socket.socket()
    s.bind(('', PORT))
    s.listen(1)
    print("WebSocket server listening on port", PORT)

    while True:
        conn, addr = s.accept()
        print("Client connected:", addr)
        data = conn.recv(1024).decode()
        try:
            cmd = ujson.loads(data)
            if "ir" in cmd:
                send_ir_command(cmd["ir"])
        except Exception as e:
            print("Error:", e)
        conn.close()


def sensor_loop():
    while True:
        if read_pir():
            print("Motion detected!")
        dist = read_ultrasonic()
        print("Distance:", dist)
        head, belly = read_touch()
        print("Head:", head, "Belly:", belly)
        time.sleep(1)


connect_wifi()
_thread.start_new_thread(websocket_server, ())
sensor_loop()
