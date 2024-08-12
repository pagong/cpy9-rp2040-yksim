# Test YKSIM with JSON file io

import json

DIR = "/yk-ids"
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

dfltfile = DIR + "/" + DEF + SFX
defaults = read_json_dict(dfltfile)

cfgfile = defaults["directory"] + defaults["config"] + defaults["public"] + SFX
ykcfg = read_json_dict(cfgfile)

sesfile = defaults["directory"] + ykcfg["session"] + ykcfg["public"] + SFX
sesctr = read_json_dict(sesfile)

#################

from yubiotp.otp import OTP, encode_otp, decode_otp, YubiKey
from yubiotp.modhex import is_modhex, modhex, unmodhex

#################

def update_session(counter):
    #global sesctr, sesfile
    sesctr["counter"] = counter
    try:
        write_json_dict(sesfile, sesctr)
    except Exception as e:
        #print(e)
        pass

aeskey = ykcfg["aeskey"].encode()
private = ykcfg["private"].encode()
public = ykcfg["public"].encode()

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

usrbtn = DigitalInOut(board.GP29)
usrbtn.direction = Direction.INPUT
usrbtn.pull = Pull.UP
switch = Debouncer(usrbtn)

def delay(count):
    for i in range(count):
        time.sleep(0.1)
        switch.update()

pixels = neopixel.NeoPixel(board.GP16, 1, pixel_order=neopixel.RGB)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
OFF = (0, 0, 0)

colors = [RED, GREEN, BLUE]
index = 0
WAIT = 30

def rgbled(color):
    pixels.fill(color)

def do_yksim():
    rgbled(GREEN)
    yktok = gen_token()
    keyboard.write(str(yktok, 'ascii') + "\n")
    rgbled(RED)

#################

rgbled(BLUE)   
delay(WAIT)

while True:
    switch.update()
    if not switch.value:
        #print("pressed")
        do_yksim()
        delay(WAIT)
        rgbled(BLUE)
