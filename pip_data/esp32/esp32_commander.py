from machine import UART, Pin
import time

# Setup UART on GPIO19 (TX) and GPIO20 (RX)
uart = UART(1, baudrate=115200, tx=Pin(19), rx=Pin(20))

# Optional: onboard LED indicator (adjust pin if necessary)
led = Pin(15, Pin.OUT)  # Adjust if you're using a different pin for onboard LED

def parse_command(command):
    command = command.strip()
    print("Received command:", command)

    if command == "LED_ON":
        led.value(1)
    elif command == "LED_OFF":
        led.value(0)
    elif command.startswith("SAY:"):
        message = command[4:]
        print("Message to speak:", message)
        # Forward this to audio_out if you're doing playback here
    else:
        print("Unknown command")

def listen_loop():
    buffer = b""
    while True:
        if uart.any():
            data = uart.read()
            if data:
                buffer += data
                if b"\n" in buffer:
                    lines = buffer.split(b"\n")
                    for line in lines[:-1]:
                        parse_command(line.decode().strip())
                    buffer = lines[-1]
        time.sleep(0.1)

listen_loop()
