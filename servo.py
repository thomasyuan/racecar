import RPi.GPIO as GPIO
from time import sleep

# Define GPIO pin for the servo
SERVO_PIN = 14  # GPIO 14

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Set PWM frequency to 50Hz (20ms period)
pwm = GPIO.PWM(SERVO_PIN, 50)
pwm.start(0)

def set_servo_angle(angle):
    # Convert angle to duty cycle
    duty_cycle = 2.5 + (angle / 180.0) * 10.0
    pwm.ChangeDutyCycle(duty_cycle)
    sleep(0.5)  # Allow time for the servo to move

try:
    while True:
        # Move servo to 0 degrees
        print("Moving to 0 degrees")
        set_servo_angle(0)
        sleep(1)
        
        # Move servo to 45 degrees
        print("Moving to 45 degrees")
        set_servo_angle(45)
        sleep(1)
        
        # Move servo to 90 degrees
        print("Moving to 90 degrees")
        set_servo_angle(90)
        sleep(1)
        
        # Move servo to 135 degrees
        print("Moving to 135 degrees")
        set_servo_angle(135)
        sleep(1)
        
        # Move servo to 180 degrees
        print("Moving to 180 degrees")
        set_servo_angle(180)
        sleep(1)
except KeyboardInterrupt:
    print("Servo control stopped by User")
finally:
    pwm.stop()
    GPIO.cleanup()
