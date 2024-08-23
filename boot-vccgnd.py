"""
boot.py file for Pico data logging example.

- If pin GP24 is NOT connected to GND when the pico starts up,
  make the filesystem writeable by CircuitPython.
- If pin GP24 is connected to GND when the pico starts up,
  make the filesystem writeable via USB.

https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/data-logger
"""

# for VCC-GND RP-2040

import board
import digitalio
import storage

WRpin = digitalio.DigitalInOut(board.BUTTON)
WRpin.direction = digitalio.Direction.INPUT
WRpin.pull = digitalio.Pull.UP

# If write pin is NOT connected to ground on start-up,
# CircuitPython can write to CIRCUITPY filesystem.
storage.remount("/", readonly=(not WRpin.value))
