import RPi.GPIO as GPIO
from connection import publish_status

# Define motor control pins
in1 = 24
in2 = 23
in3 = 17
in4 = 27
en1 = 4
en2 = 25
speed = 0
gear = 'P'

def set_gear(message):
    global gear
    gear = message.get("gear", 0)
    publish_status(f"Cmd: set_gear {gear}")
    set_gear_internal(gear)

def set_speed(message):
    global speed
    speed = message.get("speed", 0)
    publish_status(f"Cmd: set_speed {speed}")
    if (speed > 100):
        speed = 100
    elif (speed < 0):
        speed = 0

    set_speed_internal(speed)

def spin(message):
    direction = message.get("direction")
    publish_status(f"Cmd: spin {direction}")
    if direction == "left":
        spin_left_internal()
    elif direction == "right":
        spin_right_internal()
    elif direction == "stop":
        back_to_center_internal()

def turn(message):
    angle = message.get("angle")
    publish_status(f"Cmd: turn {angle}")
    if angle == 0:
        set_speed_internal(speed)
    elif angle < 0:
        set_left_wheels_speed(speed / (90 - abs(angle)))
    elif angle > 0:
        set_right_wheels_speed(speed / (90 - abs(angle)))


def set_gear_internal(gear):
    if gear == 'D':
        control_left_wheels(1)
        control_right_wheels(1)
    elif gear == 'R':
        control_left_wheels(-1)
        control_right_wheels(-1)
    else:
        control_left_wheels(0)
        control_right_wheels(0)

def spin_left_internal():
    publish_status("Turning left")
    stop_internal()
    control_left_wheels(1)
    control_right_wheels(-1)

def spin_right_internal():
    publish_status("Turning right")
    stop_internal()
    control_left_wheels(-1)
    control_right_wheels(1)

def back_to_center_internal():
    publish_status("Back to center")
    stop_internal()
    set_gear_internal(gear)

def stop_internal():
    control_left_wheels(0)
    control_right_wheels(0)

def set_speed_internal(duty_cycle):
    pwm1.ChangeDutyCycle(duty_cycle)
    pwm2.ChangeDutyCycle(duty_cycle)

def set_left_wheels_speed(duty_cycle):
    pwm1.ChangeDutyCycle(duty_cycle)

def set_right_wheels_speed(duty_cycle):
    pwm2.ChangeDutyCycle(duty_cycle)

def control_left_wheels(direction):
    if direction == 1:
        GPIO.output(in2, GPIO.HIGH)
        GPIO.output(in1, GPIO.LOW)
    elif direction == -1:
        GPIO.output(in2, GPIO.LOW)
        GPIO.output(in1, GPIO.HIGH)
    else:
        GPIO.output(in2, GPIO.LOW)
        GPIO.output(in1, GPIO.LOW)

def control_right_wheels(direction):
    if direction == 1:
        GPIO.output(in3, GPIO.HIGH)
        GPIO.output(in4, GPIO.LOW)
    elif direction == -1:
        GPIO.output(in3, GPIO.LOW)
        GPIO.output(in4, GPIO.HIGH)
    else:
        GPIO.output(in3, GPIO.LOW)
        GPIO.output(in4, GPIO.LOW)

def initialize_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(in1, GPIO.OUT)
    GPIO.setup(in2, GPIO.OUT)
    GPIO.setup(in3, GPIO.OUT)
    GPIO.setup(in4, GPIO.OUT)
    GPIO.setup(en1, GPIO.OUT)
    GPIO.setup(en2, GPIO.OUT)

    global pwm1, pwm2, direction
    pwm1 = GPIO.PWM(en1, 1000)  # PWM frequency 1000 Hz
    pwm2 = GPIO.PWM(en2, 1000)  # PWM frequency 1000 Hz
    pwm1.start(0)
    pwm2.start(0)
    direction = 0
    control_left_wheels(0)
    control_right_wheels(0)
    set_speed_internal(speed)

def start():
    print("Starting the car")
    initialize_gpio()

def exit():
    stop_internal()
    GPIO.cleanup()
