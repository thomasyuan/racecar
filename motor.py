import RPi.GPIO as GPIO
import asyncio
import time
import gyro
from controller import register_command
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
    publish_status(f"Setting gear to {gear}")
    set_gear_internal(gear)

def set_speed(message):
    global speed
    speed = message.get("speed", 0)
    publish_status(f"Setting speed to {speed}")
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

# Initialize variables
current_angle = 0.0
previous_time = time.time()
target_angle = 90.0  # Target angle in degrees
gyro_sensitivity = 1.0  # Sensitivity factor for the gyro (depends on your sensor)


def turn_left_internal():
    publish_status("Turning left")
    stop_internal()
    control_left_wheels(1)
    control_right_wheels(-1)

async def turn_right_internal():
    # publish_status("Turning right")
    # stop_internal()
    # control_left_wheels(-1)
    # control_right_wheels(1)
    global current_angle, previous_time

    publish_status("Turning right")
    stop_internal()
    control_left_wheels(-1)
    control_right_wheels(1)

    while current_angle < target_angle:
        # Simulate reading gyro data
        gyro_x, gyro_y, gyro_z = await read_gyro_data()  # Replace with actual gyro reading function

        # Calculate the time difference
        current_time = time.time()
        dt = current_time - previous_time
        previous_time = current_time

        # Integrate the angular velocity to get the angle
        angular_velocity_z = gyro_z * gyro_sensitivity
        current_angle += angular_velocity_z * dt

        # Print the gyro data and current angle
        print(f"Gyro X: {gyro_x}, Gyro Y: {gyro_y}, Gyro Z: {gyro_z}, Angle: {current_angle:.2f}")

        await asyncio.sleep(0.01)  # Small delay to simulate sensor reading interval

    # Stop the turn when the target angle is reached
    stop_internal()
    publish_status("Turned 90 degrees!")
    current_angle = 0.0  # Reset the angle

async def read_gyro_data():
    # Replace this with actual code to read gyro data
    # For example, you might use an I2C library to read from an MPU6050 sensor
    return gyro.read_gyro_data()

def back_to_center_internal():
    # if direction == 0:
    #     return
    publish_status("Back to center")
    stop_internal()
    set_gear_internal(gear)

def stop_internal():
    publish_status("Center")
    control_left_wheels(0)
    control_right_wheels(0)

def set_speed_internal(duty_cycle):
    pwm1.ChangeDutyCycle(duty_cycle)
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

    gyro.initialize_gyro()

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
