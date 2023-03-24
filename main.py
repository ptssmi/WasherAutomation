import RPi.GPIO as GPIO
import time

# Set which GPIO pins will handle each input
START_LED = 38
LOCK_LED  = 36
SPIN_LED  = 32
DONE_LED  = 26

# Configure GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(START_LED, GPIO.IN)
GPIO.setup(LOCK_LED, GPIO.IN) 
GPIO.setup(SPIN_LED, GPIO.IN) 
GPIO.setup(DONE_LED, GPIO.IN)

# Monitor the status of voltage
while True:
  if GPIO.input(DONE_LED):
    print("ON")
  else:
    print("OFF")
  time.sleep(0.1)

# Cleanup once program terminates
GPIO.cleanup()
