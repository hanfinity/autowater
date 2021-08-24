# External module imp
import RPi.GPIO as GPIO
import datetime
import time

init = False

GPIO.setmode(GPIO.BOARD) # Broadcom pin-numbering scheme

def get_last_watered():
    try:
        f = open("last_watered.txt", "r")
        return f.readline()
    except:
        return "NEVER!"
      
def get_status(pin = 8):
    GPIO.setup(pin, GPIO.IN) 
    return GPIO.input(pin)

def init_output(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    #GPIO.output(pin, GPIO.HIGH)

def pump_off(pin = 7):
    GPIO.setup(pin, GPIO.IN)
   
# water the plant until the drip tray is wet
def auto_water(delay = 5, pump_pin = 7, water_sensor_pin = 8):
    consecutive_water_count = 0
    wet = False
    pump_on(pump_pin, 60)
    while not wet:
        pump_on(pump_pin, delay)
        time.sleep(delay)
        consecutive_water_count += 1
        wet = get_status(pin = water_sensor_pin) == 0
    GPIO.cleanup() # cleanup all GPI

def pump_on(pump_pin = 7, delay = 5):
    init_output(pump_pin)
    f = open("last_watered.txt", "w")
    f.write("Last watered {}".format(datetime.datetime.now()))
    f.close()
    GPIO.output(pump_pin, GPIO.HIGH)
    time.sleep(delay)
    GPIO.setup (pump_pin, GPIO.IN)

