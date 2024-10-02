import time
import threading
from gpiozero import DistanceSensor
from gpiozero.pins.pigpio import PiGPIOFactory
import controller  # Import the controller module

from utils import start_daemon_thread  # Import the start_daemon_thread function

# Set the pin factory to use RPi.GPIO
factory = PiGPIOFactory()

# Define GPIO pins for the ultrasonic sensor
TRIG_PIN = 5  # GPIO 5
ECHO_PIN = 6  # GPIO 6

# Define the interval for reading the sensor in the monitoring loop
MONITOR_READING_INTERVAL = 0.05

# Create a stop event
stop_event = threading.Event()

# Initialize the DistanceSensor with the specified pin factory
sensor = DistanceSensor(echo=ECHO_PIN, trigger=TRIG_PIN, pin_factory=factory)

def get_distance():
    try:
        distance = sensor.distance * 100  # Convert to cm
        return distance
    except Exception as e:
        print(f"Error getting distance: {e}")
        return None

# def get_average_distance(samples=5):
#     distances = []
#     for _ in range(samples):
#         distance = get_distance()
#         if distance is not None:
#             distances.append(distance)
#         time.sleep(0.05)  # Small delay between samples

#     if distances:
#         return sum(distances) / len(distances)
#     else:
#         return None

def monitor_ultrasonic(interval):
    while True:
        distance = get_distance()
        if distance is not None:
            print(f"Distance: {distance} cm")
            controller.handle_ultrasonic(distance)
        else:
            print("Failed to get distance")
        time.sleep(interval)

def monitor_ultrasonic():
    while not stop_event.is_set():
        distance = get_distance()
        if distance is not None:
            # print(f"Distance: {distance} cm")
            controller.handle_ultrasonic(distance)
        else:
            print("Failed to get distance")
        time.sleep(MONITOR_READING_INTERVAL)

# Example usage
if __name__ == "__main__":
    try:
        while True:
            distance = get_distance()
            if distance is not None:
                print(f"Distance: {distance} cm")
            else:
                print("Failed to get distance")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Measurement stopped by User")
    finally:
        sensor.close()

def start():
    # Initialize GPIO
    stop_event.clear()
    start_daemon_thread(monitor_ultrasonic)

def exit():
    print("Stopping ultrasonic sensor")
    stop_event.set()
    sensor.close()
