# esp32_motor_ir.py

from machine import Pin
import time

IR_PIN = Pin(17, Pin.OUT)


def send_pulse():
    IR_PIN.on()
    time.sleep_us(560)
    IR_PIN.off()
    time.sleep_us(560)


def send_ir_command(command):
    if command == "FORWARD":
        hex_code = 0x21
    elif command == "REVERSE":
        hex_code = 0x28
    elif command == "LEFT":
        hex_code = 0x22
    elif command == "RIGHT":
        hex_code = 0x24
    else:
        return
    print("Sending IR:", command)
    for i in range(16):
        if (hex_code >> i) & 1:
            send_pulse()
        time.sleep_us(500)
