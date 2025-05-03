# esp32_ws_ir_server.py
# MicroPython WebSocket server for receiving commands from Pip's AI

import uasyncio as asyncio
import machine
import time

# Configure IR LED on GPIO17
IR_PIN = 17
ir_led = machine.Pin(IR_PIN, machine.Pin.OUT)


def _pulse_ir(pattern):
    for mark, space in pattern:
        ir_led.on()
        time.sleep_us(mark)
        ir_led.off()
        time.sleep_us(space)


def send_ir_command(name):
    print(f"[ESP32 IR] Command received: {name}")
    if name == "SPIN_FAST":
        _pulse_ir([
            (9000, 4500),
            (560, 560), (560, 1690), (560, 560),
        ])
    elif name == "HEADPAT_HAPPY":
        _pulse_ir([
            (9000, 4500),
            (560, 1690), (560, 560), (560, 560),
        ])
    else:
        print("[ESP32 IR] Unknown command")


async def serve(reader, writer):
    print("[ESP32 WS] New client connected")
    try:
        while True:
            data = await reader.read(512)
            if not data:
                break
            message = data.decode().strip()
            print(f"[ESP32 WS] Message: {message}")
            send_ir_command(message)
    except Exception as e:
        print(f"[ESP32 WS] Error: {e}")
    finally:
        await writer.aclose()


async def main():
    print("[ESP32 WS] Starting WebSocket IR server...")
    server = await asyncio.start_server(serve, "0.0.0.0", 8266)
    async with server:
        await server.serve_forever()


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Server stopped.")
