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

def turn_right(message):
    degree = message.get("degree", 0)
    print(f"Turning right by {degree} degrees")
    turn_right_internal()
    # Implement the logic to turn the car right by the specified degree

def turn_left(message):
    degree = message.get("degree", 0)
    print(f"Turning left by {degree} degrees")
    turn_left_internal()
    # Implement the logic to turn the car left by the specified degree

def set_speed(message):
    global speed
    speed = message.get("speed", 0)
    print(f"Setting speed to {speed}")
    if (speed > 100):
        speed = 100
    elif (speed < 0):
        speed = 0

    set_speed_internal(speed)
    # Implement the logic to set the car's speed

def go_forward(message):
    print("Going forward")
    # stop_internal()
    # global direction
    # if direction == -1:
    #     sleep(0.5)
    direction = 1
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)

def go_backward(message):
    print("Going backward")
    # stop_internal()
    # global direction
    # if direction == 1:
    #     sleep(0.5)
    direction = -1
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)

def stop(message):
    global direction
    direction = 0
    stop_internal()

def turn_right_internal():
    # stop_internal()
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)
    #sleep(0.5)

def turn_left_internal():
    # stop_internal()
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    # sleep(0.5)


def stop_internal():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)


def set_speed_internal(duty_cycle):
    pwm1.ChangeDutyCycle(duty_cycle)
    pwm2.ChangeDutyCycle(duty_cycle)

def continue_running(message):
    stop_internal()
    if direction == 1:
        go_forward(message)
    elif direction == -1:
        go_backward(message)
    else:
        stop_internal()

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
    set_speed_internal(speed)


def start():
    print("Starting the car")
    initialize_gpio()

def exit():
    stop_internal()
    GPIO.cleanup()

# Register commands
register_command("turn_right", turn_right)
register_command("turn_left", turn_left)
register_command("set_speed", set_speed)
register_command("go_forward", go_forward)
register_command("go_backward", go_backward)
register_command("stop", stop)
register_command("continue_running", continue_running)
