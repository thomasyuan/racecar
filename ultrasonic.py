import RPi.GPIO as GPIO
import time
import threading
import controller  # Import the controller module

from utils import start_daemon_thread  # Import the start_daemon_thread function

# Define GPIO pins for the ultrasonic sensor
TRIG_PIN = 5  # GPIO 5
ECHO_PIN = 6  # GPIO 6


# Define the interval for reading the sensor in the monitoring loop
MONITOR_READING_INTERVAL = 0.05

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

# Create a stop event
stop_event = threading.Event()

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

def monitor_ultrasonic():
    while not stop_event.is_set():
        distance = get_distance()
        controller.handle_ultrasonic(distance)
        time.sleep(MONITOR_READING_INTERVAL)

def start():
    stop_event.clear()
    start_daemon_thread(monitor_ultrasonic)

def exit():
    stop_event.set()
    GPIO.cleanup()

def main():
    try:
        while True:
            distance = get_distance()
            print(f"Distance: {distance} cm")
            time.sleep(MONITOR_READING_INTERVAL)
    except KeyboardInterrupt:
        print("Measurement stopped by User")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    MONITOR_READING_INTERVAL = 1
    main()