import RPi.GPIO as GPIO

MOTOR_PIN = 18

def initialize_motor():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(MOTOR_PIN, GPIO.OUT)

def control_motor(action):
    if action == 'stop':
        GPIO.output(MOTOR_PIN, GPIO.LOW)
    elif action == 'move':
        GPIO.output(MOTOR_PIN, GPIO.HIGH)