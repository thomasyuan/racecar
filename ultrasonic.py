import RPi.GPIO as GPIO
import time
from threading import Lock

# Define GPIO pins for the ultrasonic sensor
TRIG_PIN = 5  # GPIO 5
ECHO_PIN = 6  # GPIO 6

# Define threshold distance in cm
DISTANCE_THRESHOLD = 300  # 3 meters

# Define the interval for reading the sensor in the monitoring loop
MONITOR_READING_INTERVAL = 0.1

# Define the interval for reading the sensor in the main loop
MAIN_READING_INTERVAL = 1

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

# Create a lock object
lock = Lock()

def get_distance():
    # Send a 10us pulse to trigger
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    # Wait for the echo to start
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()

    # Wait for the echo to end
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    # Calculate the distance
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Speed of sound in cm/s
    distance = round(distance, 2)
    return distance

def read_ultrasonic_sensor():
    return get_distance()

def main():
    try:
        while True:
            with lock:
                distance = read_ultrasonic_sensor()
                print(f"Distance: {distance} cm")
            time.sleep(MAIN_READING_INTERVAL)
    except KeyboardInterrupt:
        print("Measurement stopped by User")
    finally:
        GPIO.cleanup()

def monitor_ultrasonic():
    while True:
        with lock:
            distance = get_distance()
            print(f"Distance: {distance} cm")
            if distance < DISTANCE_THRESHOLD:  # Compare with threshold in cm
                print("Obstacle detected! Turning right.")
                # set_servo_angle(90)  # Turn right
        time.sleep(MONITOR_READING_INTERVAL)

def start_monitoring():
    import threading
    thread = threading.Thread(target=monitor_ultrasonic)
    thread.daemon = True
    thread.start()
    return thread

if __name__ == "__main__":
    main()