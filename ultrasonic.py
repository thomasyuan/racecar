from gpiozero import DistanceSensor
from time import sleep

# Define GPIO pins for the ultrasonic sensor
TRIG_PIN = 5  # GPIO 5
ECHO_PIN = 6  # GPIO 6

# Define threshold distance in cm
DISTANCE_THRESHOLD = 0.3  # gpiozero uses meters

# Define the interval for reading the sensor in the monitoring loop
MONITOR_READING_INTERVAL = 0.1

# Define the interval for reading the sensor in the main loop
MAIN_READING_INTERVAL = 1

# Initialize the DistanceSensor
sensor = DistanceSensor(echo=ECHO_PIN, trigger=TRIG_PIN)

def get_distance():
    # Get the distance in meters and convert to cm
    distance = sensor.distance * 100
    return round(distance, 2)

def read_ultrasonic_sensor():
    return get_distance()

def main():
    try:
        while True:
            distance = read_ultrasonic_sensor()
            print(f"Distance: {distance} cm")
            sleep(MAIN_READING_INTERVAL)
    except KeyboardInterrupt:
        print("Measurement stopped by User")

def monitor_ultrasonic():
    while True:
        distance = get_distance()
        print(f"Distance: {distance} cm")
        if distance < DISTANCE_THRESHOLD * 100:  # Convert threshold to cm
            print("Obstacle detected! Turning right.")
            # set_servo_angle(90)  # Turn right
        sleep(MONITOR_READING_INTERVAL)

def start_monitoring():
    import threading
    thread = threading.Thread(target=monitor_ultrasonic)
    thread.daemon = True
    thread.start()
    return thread

if __name__ == "__main__":
    main()