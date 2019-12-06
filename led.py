import RPi.GPIO as GPIO


def turn_on_led(pin_number):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()
    GPIO.setup(pin_number, GPIO.OUT)
    GPIO.output(pin_number, GPIO.HIGH)


def turn_off_led():
    GPIO.cleanup()
