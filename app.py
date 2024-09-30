import threading
import time
import connection
import motor
import RPi.GPIO as GPIO

from utils import start_daemon_thread

# Define threshold distance in cm
DISTANCE_THRESHOLD = 30



if __name__ == "__main__":
    try:
        # Start the status update thread
        start_daemon_thread(connection.send_status_updates)

        # Start the ultrasonic monitoring thread
        start_daemon_thread(monitor_ultrasonic)


        # Main thread will handle other tasks or just keep the program running
        while True:
            pass  # Do nothing, just keep the main thread alive
    except KeyboardInterrupt:
        print("Exiting...")
        connection.pubnub.unsubscribe_all()
        GPIO.cleanup()  # Clean up GPIO on exit