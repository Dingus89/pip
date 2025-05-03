# sensor_handlers.py

from machine import Pin
from capacitance_sensor import CapacitiveTouchSensor

pir = Pin(13, Pin.IN)
ultrasonic_trig = Pin(14, Pin.OUT)
ultrasonic_echo = Pin(15, Pin.IN)

belly_sensor = CapacitiveTouchSensor(32)
head_sensor = CapacitiveTouchSensor(33)


def check_motion():
    return pir.value()


def check_ultrasonic():
    import time
    ultrasonic_trig.off()
    time.sleep_us(2)
    ultrasonic_trig.on()
    time.sleep_us(10)
    ultrasonic_trig.off()
    while ultrasonic_echo.value() == 0:
        signaloff = time.ticks_us()
    while ultrasonic_echo.value() == 1:
        signalon = time.ticks_us()
    time_passed = signalon - signaloff
    distance = (time_passed * 0.0343) / 2
    return distance


def check_capacitance():
    return {
        "belly": belly_sensor.is_touched(),
        "head": head_sensor.is_touched()
    }
