"""
boot.py file for Pico data logging example.

- If pin GP29 is NOT connected to GND when the pico starts up,
  make the filesystem writeable by CircuitPython.
- If pin GP29 is connected to GND when the pico starts up,
  make the filesystem writeable via USB.

https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/data-logger
"""

# for Waveshare RP2040-One

import board
import digitalio
import storage

WRpin = digitalio.DigitalInOut(board.GP29)
WRpin.direction = digitalio.Direction.INPUT
WRpin.pull = digitalio.Pull.UP

# If write pin is NOT connected to ground on start-up,
# CircuitPython can write to CIRCUITPY filesystem.
storage.remount("/", readonly=(not WRpin.value))
