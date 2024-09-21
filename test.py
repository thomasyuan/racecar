# Python Script
# https://www.electronicshub.org/raspberry-pi-l298n-interface-tutorial-control-dc-motor-l298n-raspberry-pi/

import RPi.GPIO as GPIO
import time
from time import sleep
from gpiozero import DistanceSensor

in1 = 17
in2 = 27
in3 = 23
in4 = 24
en1 = 4
en2 = 25

TRIG = 5
ECHO = 6

sensor = DistanceSensor(echo=ECHO, trigger=TRIG)

def read_ultrasonic_sensor():
    distance = sensor.distance * 100
    distance = round(distance, 2)
    return distance

def set_speed(duty_cycle):
    pwm1.ChangeDutyCycle(duty_cycle)
    pwm2.ChangeDutyCycle(duty_cycle)

def stop_internal():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)

def stop():
    global direction
    direction = 0
    stop_internal()

def go_forward():
    stop_internal()
    global direction
    if direction == -1:
        sleep(0.5)
    direction = 1
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)

def go_backward():
    stop_internal()
    global direction
    if direction == 1:
        sleep(0.5)
    direction = -1
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)

def turn_right():
    stop_internal()
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)
    #sleep(0.5)

def turn_left():
    stop_internal()
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    sleep(0.5)

def continue_running():
    stop_internal()
    if direction == 1:
        go_forward()
    elif direction == -1:
        go_backward()
    else:
        stop()

def initialize_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(in1,GPIO.OUT)
    GPIO.setup(in2,GPIO.OUT)
    GPIO.setup(in3,GPIO.OUT)
    GPIO.setup(in4,GPIO.OUT)
    GPIO.setup(en1,GPIO.OUT)
    GPIO.setup(en2,GPIO.OUT)
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

def usage():
    print("Usage:")
    print("p: Power on")
    print("a: Auto mode")
    print("f: Go forward")
    print("b: Go backward")
    print("l: Turn left")
    print("r: Turn right")
    print("s: Stop")
    print("m: Medium speed")
    print("h: High speed")
    print("q: Quit")

def main():
    try:
        initialize_gpio()
        usage()

        while True:
            x = input("Enter command: ")
            if x == 'p':
                print("Power on")
                set_speed(70)
            if x == 's':
                print("Stop")
                stop()
            elif x == 'f':
                print("Going forward")
                go_forward()
            elif x == 'b':
                print("Going backward")
                go_backward()
            elif x == 'l':
                print("Turning left")
                turn_left()
                continue_running()
            elif x == 'r':
                print("Turning right")
                turn_right()
                continue_running()
            elif x == 'm':
                print("Medium speed")
                set_speed(70)
            elif x == 'h':
                print("High speed")
                set_speed(100)
            elif x == 'q':
                print("Quit")
                break
            elif x == 'a':
                print("auto mode")
                go_forward()
                try:
                    while True:
                        distance = read_ultrasonic_sensor()
                        print(f"distance {distance} cm")
                        if distance < 30:
                            turn_right()
                        else:
                            continue_running()
                except KeyboardInterrupt:
                    print("Measurement stopped by User")
            else:
                print("Invalid command")
    except KeyboardInterrupt:
        print("Measurement stopped by User")
    finally:
        pwm1.stop()
        pwm2.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    main()
