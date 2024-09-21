from gpiozero import DistanceSensor, Motor, PWMOutputDevice
from time import sleep

# Define GPIO pins
en2 = 25

TRIG = 5
ECHO = 6

# Initialize DistanceSensor
sensor = DistanceSensor(echo=ECHO, trigger=TRIG)

# Initialize Motors
motor_left = Motor(forward=17, backward=27)
motor_right = Motor(forward=23, backward=24)

# Initialize PWM for speed control
pwm_left = PWMOutputDevice(4)
pwm_right = PWMOutputDevice(25)

def read_ultrasonic_sensor():
    distance = sensor.distance * 100
    distance = round(distance, 2)
    return distance

def set_speed(duty_cycle):
    pwm_left.value = duty_cycle / 100
    pwm_right.value = duty_cycle / 100

def stop_internal():
    motor_left.stop()
    motor_right.stop()

def stop():
    global direction
    direction = 0
    stop_internal()

def go_forward():
    global direction
    direction = 1
    motor_left.forward()
    motor_right.forward()

def go_backward():
    global direction
    direction = -1
    motor_left.backward()
    motor_right.backward()

def turn_left():
    motor_left.backward()
    motor_right.forward()
    sleep(0.2)
    stop_internal()

def turn_right():
    motor_left.forward()
    motor_right.backward()
    sleep(0.2)
    stop_internal()

def usage():
    print("Usage:")
    print("p: Power on")
    print("f: Go forward")
    print("b: Go backward")
    print("l: Turn left")
    print("r: Turn right")
    print("s: Stop")
    print("e: Exit")

def main():
    try:
        usage()

        while True:
            x = input("Enter command: ")

            if x == 'p':
                print("Power on")
                set_speed(100)  # Full speed
            elif x == 's':
                print("Stopping")
                stop()
                set_speed(0)  # Stop PWM
            elif x == 'f':
                print("Going forward")
                go_forward()
            elif x == 'b':
                print("Going backward")
                go_backward()
            elif x == 'l':
                print("Turning left")
                turn_left()
                go_forward()
            elif x == 'r':
                print("Turning right")
                turn_right()
                go_forward()
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
                        print(f"Distance: {distance} cm")
                        if distance < 30:
                            turn_right()
                            go_forward()  # Continue moving forward after turning
                        sleep(0.1)  # Add a small delay to stabilize the loop
                except KeyboardInterrupt:
                    print("Measurement stopped by User")
                    stop()
            else:
                print("Invalid command")
    except KeyboardInterrupt:
        print("Measurement stopped by User")
    finally:
        stop()

if __name__ == "__main__":
    main()