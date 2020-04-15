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

right = Motor(Port.D)
left = Motor(Port.A)

ford = DriveBase(left, right, 56, 90)

color = ColorSensor(Port.S1)

ROGERS = passwords.Key1
STRONG = passwords.Key2

## SYSTEM LINK CODE TAKEN FROM MIDTERM
def setup_systemlink(key):
    #print("SETTUP FOR SYSTEMLINK")
    urlBase = "https://api.systemlinkcloud.com/nitag/v2/tags/"
    headers = {"Accept": "application/json", "x-ni-api-key": key}
    return urlBase, headers

def send_to_system_link(Tag, Type, Value, key):
    print("Sending to system link")
    urlBase, headers = setup_systemlink(key)
    urlVal = urlBase + Tag + "/values/current"
    propVal = {"value":{"type": Type, "value": Value}}
    try:
        reply = urequests.put(urlVal, headers = headers, json = propVal).text
    except Exception as e:
        print(e)
        reply = 'failed'
    return reply  

def get_from_system_link(Tag,key):
    urlBase, headers = setup_systemlink(key)
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
    onMat = color.reflection()
    #onMat = color.color()
    print(onMat)
    while onMat >= 3:
    #while onMat != Color.BLUE():
        ## rotate a bit right
        print('TURN RIGHT')
        ford.drive(10, -50)
        wait(100)
        onMat = color.reflection()
        #onMat = color.color()
        print(onMat)
        if onMat >= 3:
            ## rotate a bit left
            print('TURN LEFT')
            ford.drive(15,50)
            wait(200) ## turn back then turn some more
            onMat = color.reflection()
            #onMat = color.color()
    ford.drive(-15, 0)

go = False
while go != False:
    go = get_from_system_link('Start19', ROGERS)
    print(go)
    
dinoFlag4 = 0
while dinoFlag4 == 0:
    driveCar()
    wait(100)
    dinoFlag4 = int(get_from_system_link('dino4', STRONG))
    print('dinoFlag is', dinoFlag4)

print("DONE!")
#send_to_system_link('Start20', 'BOOLEAN', 'true', ROGERS)
#send_to_system_link('Start19', 'BOOLEAN', 'false', ROGERS)
