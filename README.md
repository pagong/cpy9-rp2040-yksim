# cpy9-rp2040-yksim

YubiKey simulator for Raspberry Pi Picos and similar boards.

After having created the original [arduino-yksim](https://github.com/pagong/arduino-yksim) ten years ago,
I wanted to learn about CircuitPython and at the same time use the "RPi Pico" in a useful project.

## Hardware
I've used the "RP2040-One" and "RP2040-Zero" (by WaveShare) for the first versions.
Both modules are tiny in size and have an on-board NeoPixel LED.

## Preparation

First you need to install "CircuitPython 9" to your RP2040 board. Go to the [download](https://circuitpython.org/downloads)
page and select the version that is suitable for your module. If you are unfamiliar with installing `UF2` firmware,
you should be starting at Adafruit's [learn](https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython) page.

Second, you need to add a push button between GND and a digital IO pin of your RP2040 board.
- I've soldered one to Pin `GP29` and `GND` of the 'WaveShare' boards.
- On the original "RPi Pico" Pin `GP15` and `GND` are conveniently located at the end ot the module.
- For the cheap "YD-RP2040" board no additional button is needed, as there is alreay a `USR` button at `GP24`.

## Design
The code of _YKSIM_ is written in CircuitPython 9 and has several libraries as dependencies. Some of them are standard libraries 
of CircuitPython. Others need to be copied from the Adafruit (`adafruit-circuitpython-bundle-9.x-mpy-<date>.zip`) and 
Community (`circuitpython-community-bundle-9.x-mpy-<date>.zip`) bundles to the `/lib` folder of the `CIRCUITPY` drive.
Both library bundles can be downloaded from the CircuitPython [libraries](https://circuitpython.org/libraries) page.

``` bash
$ ls -l lib/
total 36
-rw-r--r-- 1 msd users 15686 Jul 30 05:15 adafruit_datetime.mpy
-rw-r--r-- 1 msd users  2025 Jul 30 05:15 adafruit_debouncer.mpy
drwxr-xr-x 1 msd users   270 Aug  9 23:52 adafruit_hid
-rw-r--r-- 1 msd users  2796 Jul 30 05:15 adafruit_pixelbuf.mpy
-rw-r--r-- 1 msd users   634 Jul 30 05:15 adafruit_ticks.mpy
-rw-r--r-- 1 msd users   718 Aug  6 05:15 circuitpython_functools.mpy
-rw-r--r-- 1 msd users  1318 Jul 30 05:15 neopixel.mpy
```

| script name | needs these libraries | and these dependencies |
| --- | --- | --- |
| crc.py | -- | -- |
| modhex.py | binascii<br>struct<br>circuitpathon_functools | -- |
| otp.py | binascii<br>struct<br>random<br>aesio<br>adafruit_datetime | -- |
| --- | --- | --- |
| boot.py | board<br>digitalio<br>storage | -- |
| code.py | json<br>time<br>board<br>usb_hid | adafruit_hid |
| code.py | neopixel<br>adafruit_debouncer | adafruit_pixelbuf<br>adafruit_ticks |


``` python /yubiotp/modhex.py
from binascii import hexlify, unhexlify
from circuitpython_functools import partial
import struct
```

``` python /yubiotp/otp.py
from binascii import hexlify
from adafruit_datetime import datetime
from random import randrange
from struct import pack, unpack
import aesio
from yubiotp.crc import crc16, verify_crc16
from yubiotp.modhex import is_modhex, modhex, unmodhex
```

``` python /boot.py
import board
import digitalio
import storage
```

``` python /code.py
import json
from yubiotp.otp import OTP, encode_otp, decode_otp, YubiKey
from yubiotp.modhex import is_modhex, modhex, unmodhex
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
import time
import board
import neopixel
from digitalio import DigitalInOut, Direction, Pull
from adafruit_debouncer import Debouncer
```

``` python
```

``` python
```

``` python
```

``` python
```

