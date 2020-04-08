#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import ubinascii, ujson, urequests, utime
import passwords


# Write your program here
ev3 = EV3Brick()
ev3.speaker.beep()

right = Motor.Port(D)
left = Motor.Port(A)

ford = DriveBase(left, right, 56, 90)

color = colorSensor.Port(S1)


Key = passwords.Keys[Key]

## SYSTEM LINK CODE TAKEN FROM MIDTERM
def setup_systemlink():
    #print("SETTUP FOR SYSTEMLINK")
    urlBase = "https://api.systemlinkcloud.com/nitag/v2/tags/"
    headers = {"Accept": "application/json", "x-ni-api-key": Key}
    return urlBase, headers

def send_to_system_link(Tag, Type, Value):
    print("Sending to system link")
    urlBase, headers = setup_systemlink()
    urlVal = urlBase + Tag + "/values/current"
    propVal = {"value":{"type": Type, "value": Value}}
    try:
        reply = urequests.put(urlVal, headers = headers, json = propVal).text
    except Exception as e:
        print(e)
        reply = 'failed'
    return reply  

def get_from_system_link(Tag):
    urlBase, headers = setup_systemlink()
    urlVal = urlBase + Tag + "/values/current"
    try:
        value = urequests.get(urlVal, headers = headers).text
        data = ujson.loads(value)
        #print(data)
        result = data.get("value").get("value")
    except Exception as e:
        print(e)
        result = 'failed'
    return result

def driveCar():
    onMat = color.Color()
    if onMat != (Color.GREEN or Color.BLUE):
        drive

go = False
while go == False:
    go = get_from_system_link('Start19')

while go == True:
    