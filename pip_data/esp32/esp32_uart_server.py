import machine
import time

uart = machine.UART(1, tx=19, rx=20, baudrate=115200)

print("UART server running...")

while True:
    if uart.any():
        data = uart.readline()
        if data:
            print("Received:", data.decode().strip())
