# cpy9-rp2040-yksim
YubiKey simulator for Raspberry Pi Picos and similar boards.

After having created the original [arduino-yksim](https://github.com/pagong/arduino-yksim) ten years ago,
I wanted to learn about CircuitPython and at the same time use the "RasPi Pico" in a useful project.

## Hardware
I've used the "RP2040-One" and "RP2040-Zero" boards (by 'WaveShare') during development of _YKSIM_.
Both modules are tiny in size and have an on-board NeoPixel LED.

Other RP2040 boards can also be used, but then `code.py` needs to be adapted to their GPIO pin layouts.

The _YKSIM_ implementation makes use of the USB-HID keyboard features of CircuitPython.
Each button press generates a new YubiKey OTP token, which gets send to your connected PC.

## Preparation
First you need to install "CircuitPython 9" to your RP2040 board. Go to the [download](https://circuitpython.org/downloads)
page and select the version that is suitable for your module. If you are unfamiliar with installing `UF2` firmware,
you should be starting at Adafruit's [learn](https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython) page.

Second, you need to add a push button between GND and a digital IO pin of your RP2040 board.
- I've soldered one to Pin `GP29` and `GND` of the 'WaveShare' boards.
- On the original "RasPi Pico" Pin `GP15` and `GND` are conveniently located at the end ot the module.
However, as the "Pico" does not have an on-board RGB LED, you need to add one as well.
- For the cheap "YD-RP2040" board no additional button is needed, as there is alreay a `USR` button at `GP24`.

This push button serves dual purposes:
- Pressing the button starts the computation of a YubiKey OTP token, which gets send to your PC via USB as a series of keyboard codes.
'Yubico' has selected the so-called 'modhex' encoding, to ensure that "YubiKeys" are compatible with most keyboard layouts.
- During normal operation of _YKSIM_ the `CIRCUITPY` drive is writable by the `code.py` script. On a connected PC it gets mounted read-only!
This is accomplished with special code in `boot.py`, which gets only executed once (at reboot of a RP2040).
To make the `CIRCUITPY` drive writable via USB, you MUST keep the push button _pressed_ during boot of the `Pico`!
See this [learn](https://learn.adafruit.com/circuitpython-essentials/circuitpython-storage) page for a detailed explanation.

## Design
The code of _YKSIM_ is written in CircuitPython 9 and has several libraries as dependencies. Some of them are standard libraries 
of CircuitPython. Others need to be copied from the Adafruit (`adafruit-circuitpython-bundle-9.x-mpy-<date>.zip`) and 
Community (`circuitpython-community-bundle-9.x-mpy-<date>.zip`) bundles to the `/lib` folder of the `CIRCUITPY` drive.
Both library bundles can be downloaded from the CircuitPython [libraries](https://circuitpython.org/libraries) page.

``` bash
$ ls -l lib/
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
| boot.py | board<br>digitalio<br>storage | -- |
| code.py | json<br>time<br>board<br>digitalio | -- |
| code.py | usb_hid<br>neopixel<br>adafruit_debouncer | adafruit_hid<br>adafruit_pixelbuf<br>adafruit_ticks |
| --- | --- | --- |
| yubiotp/otp.py | binascii<br>struct<br>random<br>aesio<br>adafruit_datetime | -- |
| yubiotp/modhex.py | binascii<br>struct<br>circuitpython_functools | -- |
| yubiotp/crc.py | -- | -- |

For the YubiKey algorithm an implementation written in CPython by [django-otp](https://github.com/django-otp/yubiotp)
has been re-used and adapted for CircuitPython. Some libraries and functions have different names and parameters (e.g. `aesio`). 
(And CircuitPython does NOT like blanks in the format strings of `struct.pack` and `struct.unpack` !!)

``` bash
$ ls -l yubiotp/
-rw-r--r-- 1 msd users   919 Nov 17  2023 crc.py
-rw-r--r-- 1 msd users  2832 Aug  9 23:16 modhex.py
-rw-r--r-- 1 msd users  7156 Aug 10 06:54 otp.py
```


``` python
```


