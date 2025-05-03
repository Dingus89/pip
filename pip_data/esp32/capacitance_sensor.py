# capacitance_sensor.py

from machine import Pin, ADC


class CapacitiveTouchSensor:
    def __init__(self, pin_number, threshold=500):
        self.adc = ADC(Pin(pin_number))
        self.threshold = threshold

    def is_touched(self):
        value = self.adc.read()
        return value > self.threshold
