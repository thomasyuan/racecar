import RPi.GPIO as GPIO
from controller import register_command

# Define motor control pins
in1 = 24
in2 = 23
in3 = 17
in4 = 27
en1 = 4
en2 = 25
speed = 0


def set_gear(message):
    gear = message.get("gear", 0)
    print(f"Setting gear to {gear}")
    global direction
    if gear == 'D':
        direction = 1
        control_left_wheels(1)
        control_right_wheels(1)
    elif gear == 'R':
        direction = -1
        control_left_wheels(-1)
        control_right_wheels(-1)
    else:
        direction = 0
        control_left_wheels(0)
        control_right_wheels(0)

def set_speed(message):
    global speed
    speed = message.get("speed", 0)
    print(f"Setting speed to {speed}")
    if (speed > 100):
        speed = 100
    elif (speed < 0):
        speed = 0

    set_speed_internal(speed)

def turn(message):
    direction = message.get("direction")
    if direction == "left":
        turn_left_internal()
    elif direction == "right":
        turn_right_internal()
    elif direction == "center":
        back_to_center_internal()

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

def turn_left_internal():
    if direction == 0:
        return
    print("Turning left")
    stop_internal()
    control_left_wheels(1)
    control_right_wheels(-1)

def turn_right_internal():
    if direction == 0:
        return
    print("Turning right")
    stop_internal()
    control_left_wheels(-1)
    control_right_wheels(1)

def back_to_center_internal():
    control_left_wheels(direction)
    control_right_wheels(direction)
    
def stop_internal():
    print("center")
    control_left_wheels(direction)
    control_right_wheels(direction)

def set_speed_internal(duty_cycle):
    pwm1.ChangeDutyCycle(duty_cycle)
    pwm2.ChangeDutyCycle(duty_cycle)

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

# Register commands
register_command("turn", turn)
register_command("set_gear", set_gear)
register_command("set_speed", set_speed)
