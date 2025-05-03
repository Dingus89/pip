import socket

ESP32_IP = "192.168.4.1"  # Adjust to your ESP32 IP
ESP32_PORT = 8266


def send_to_esp32(command: str):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            s.connect((ESP32_IP, ESP32_PORT))
            s.sendall(command.encode('utf-8'))
            print(f"[PIP -> ESP32] Sent command: {command}")
    except Exception as e:
        print(f"[PIP -> ESP32] Failed to send command: {e}")
