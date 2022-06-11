# External module imp
import RPi.GPIO as GPIO
import datetime
import time
import threading
#init = False
GPIO.setmode(GPIO.BOARD) # Broadcom pin-numbering scheme

#opens the last watered.txt file and reads the line written in the document

def getLastWatered():
    try:
        f = open("Water/last_watered.txt", "r")
        return f.readline()
    except:
        return "NEVER!"
    #get last time the tap turned off
def getLastTimeTapOff():
    try:
        f = open("Water/last_tap_off.txt", "r")
        return f.readline()
    except:
        return "NEVER!"
#pin 8 is the water sensor pin this is passed in and the status is read
#returns the status of the pin input
def getStatus(pin = 8):
    GPIO.setup(pin, GPIO.IN) 
    return GPIO.input(pin)
# sets the pins for output capability on pin 7
def initOutput(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    GPIO.output(pin, GPIO.HIGH)
# sets the pins to output for the pump off pins
def initOutputOff(pin) :
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    GPIO.output(pin, GPIO.HIGH)
   #original setup water sensor pin == 0 im changing to 1
    #for testing consecutive water count is changed to 1000 times
def autoWater(running, delay = 2, pumpPin = 7, pumpPin2 = 12, pumpOffPin = 11, pumpOffPin2 = 13, waterSensorPin = 8):
    #consecutive_water_count = 0
    initOutput(pumpPin)
    initOutput(pumpPin2)
    initOutput(pumpOffPin)
    initOutput(pumpOffPin2)
    print("Here we go! Press CTRL+C to exit")
    #try:
    countTimesWatered = 0
    while countTimesWatered < 10 and running == True:
        time.sleep(delay)
        soilMoisture = getStatus(pin = waterSensorPin)
        print(soil_moisture)
        if soilMoisture == 0 and running == True:
            pumpOn(pumpPin, pumpPin2)
            time.sleep(1)
            pumpOff(pumpOffPin, pumpOffPin2)         
            countTimesWatered = countTimesWatered +1
        elif soilMoisture == 1 and running == True:
            pumpOff(pumpOffPin, pumpOffPin2)
            countTimesWatered = 0
            running = False
            break
        else:
            break
    #except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
        #GPIO.cleanup() # cleanup all GPI
def setupAuto(running, toggle):
    if toggle == "ON":
        running = True
        autoWater(running)
    else:
        running = False
        autoWater(running)
def stopAuto(running):
        running = False

def pumpOn(pumpPin = 7, pumpPin2 = 12, delay = 1):
    f = open("Water/last_watered.txt", "w")
    f.write("Last watered {}".format(datetime.datetime.now()))
    f.close()
    initOutput(pumpPin)
    initOutput(pumpPin2)
    GPIO.output(pumpPin, GPIO.LOW)
    GPIO.output(pumpPin2, GPIO.LOW)
    time.sleep(1)
    GPIO.output(pumpPin, GPIO.HIGH)
    GPIO.output(pumpPin2, GPIO.HIGH)
    time.sleep(149)
    
def pumpOff(pumpOffPin = 11, pumpOffPin2 = 13, delay = 1):
    f = open("Water/last_tap_off.txt", "w")
    f.write("tap turned off last at {}".format(datetime.datetime.now()))
    f.close()
    initOutputOff(pumpOffPin)
    initOutputOff(pumpOffPin2)
    GPIO.output(pumpOffPin, GPIO.LOW)
    GPIO.output(pumpOffPin2, GPIO.LOW)
    time.sleep(1)
    GPIO.output(pumpOffPin, GPIO.HIGH)
    GPIO.output(pumpOffPin2, GPIO.HIGH)
    
