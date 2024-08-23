# YubiKey simulator YKSIM for RP2040 boards.
# Uses the local filesystem, an USR button, USB-HID keyboard and RGB NeoPixel LED.
#
# For 'Raspberry' Pico:
# - USR button is at GP15
# - LED is at GP25

import json

DEF = "default"
SFX = ".json"

# READ key+value data from JSON
def read_json_dict(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
    return data

# WRITE key+value data to JSON
def write_json_dict(filepath, object):
    with open(filepath, 'w') as file:
        json.dump(object, file)

#################

# Put "/default.json" into root directory
dfltfile = "/" + DEF + SFX
defaults = read_json_dict(dfltfile)

# Get location of config directory from "default.json": this is usually "/yk-ids".
DIR = defaults["directory"]

cfgfile = DIR + defaults["config"] + defaults["public"] + SFX
ykcfg = read_json_dict(cfgfile)

sesfile = DIR + ykcfg["session"] + ykcfg["public"] + SFX
sesctr = read_json_dict(sesfile)

#################

# These modules are in the "/yubiotp" directory.
from yubiotp.otp import OTP, encode_otp, decode_otp, YubiKey
from yubiotp.modhex import is_modhex, modhex, unmodhex

#################

def update_session(counter):
    sesctr["counter"] = str(counter)
    try:
        write_json_dict(sesfile, sesctr)
    except Exception as e:
        #print(e)
        pass

aeskey = ykcfg["aeskey"].encode('ascii')
private = ykcfg["private"].encode('ascii')
public = ykcfg["public"].encode('ascii')

session = int(sesctr["counter"]) + 1
update_session(session)

#################

usage = 0
YK1 = YubiKey(unmodhex(private), session, usage)

def gen_token():
    global session    
    otp = YK1.generate()
    #print(str(otp))
    token = encode_otp(otp, unmodhex(aeskey), public)
    #print(str(token))
    if YK1.session != session:
        session = YK1.session
        update_session(session)
    return token

#################

import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

# init Keyboard
kbd = Keyboard(usb_hid.devices)  
keyboard = KeyboardLayoutUS(kbd)

#################

import time
import board
import neopixel

from digitalio import DigitalInOut, Direction, Pull
from adafruit_debouncer import Debouncer

#################

usrbtn = DigitalInOut(board.GP15)
usrbtn.direction = Direction.INPUT
usrbtn.pull = Pull.UP
switch = Debouncer(usrbtn)

def delay(count):
    for i in range(count):
        time.sleep(0.1)
        switch.update()

#pixels = neopixel.NeoPixel(board.RGB, 1, pixel_order=neopixel.RGB)

RED = (99, 0, 0)
GREEN = (0, 99, 0)
BLUE = (0, 0, 99)
OFF = (0, 0, 0)

colors = [RED, GREEN, BLUE]
index = 0
WAIT = 30

LED = DigitalInOut(board.LED)
LED.direction = Direction.OUTPUT


def ledon():
    LED.value = True

def ledoff():
    LED.value = False

def rgbled(color):
    pixels.fill(color)

def do_yksim():
    #rgbled(GREEN)
    yktok = gen_token()
    keyboard.write(str(yktok, 'ascii') + "\n")
    #rgbled(RED)
    ledoff()

#################

#rgbled(BLUE)   
ledon()
delay(WAIT)

while True:
    switch.update()
    if not switch.value:
        #print("pressed")
        do_yksim()
        delay(WAIT)
        #rgbled(BLUE)
	ledon()


