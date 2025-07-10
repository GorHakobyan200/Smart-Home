# from gpiozero import Servo
# from time import sleep

# servo = Servo(27)

# while (True):
#     servo.max = 180
#     sleep(1)
#     servo.min = 0
#     sleep(1)
#     servo.min = -90

import RPi.GPIO as GPIO
import time

servoPIN2 = 22
servoPIN = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)
GPIO.setup(servoPIN2, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) 
p2 = GPIO.PWM(servoPIN2, 50) 

p.start(2.5) # Initialization
p2.start(2.5)
try:
  while True:
    p2.ChangeDutyCycle(2.5)
    p.ChangeDutyCycle(2.5)
    time.sleep(1)
    p.ChangeDutyCycle(10)
    p2.ChangeDutyCycle(10)
    time.sleep(0.5)

except KeyboardInterrupt:
  p.stop()
  p2.stop()
  GPIO.cleanup()