import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

POWER_STATUS_PIN=23
GPIO.setup(POWER_STATUS_PIN, GPIO.IN)

KEY_PIN=18
GPIO.setup(KEY_PIN, GPIO.OUT)

if 0 == GPIO.input(POWER_STATUS_PIN):
        print 'Turn On'
else:
        print 'Turn Off'

GPIO.output(KEY_PIN, False)
sleep(2)
GPIO.output(KEY_PIN, True)
GPIO.cleanup()
