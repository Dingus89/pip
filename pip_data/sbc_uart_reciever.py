import serial

# Adjust to your actual device path (check with `ls /dev/ttyUSB*` or `ls /dev/ttyACM*`)
SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 115200

def handle_esp_message(message):
    print(f"[ESP] {message}")
    # Add triggers like:
    if "motion_detected" in message:
        from audio_out import speak
        speak("I see you!")

def main():
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            print(f"Listening on {SERIAL_PORT}...")
            while True:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    handle_esp_message(line)
    except serial.SerialException as e:
        print(f"Serial error: {e}")

if __name__ == "__main__":
    main()
