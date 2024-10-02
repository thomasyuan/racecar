import connection
import motor
import ultrasonic
import controller
import time

if __name__ == "__main__":
    try:
        # Start the status update thread
        connection.start()
        # Start the ultrasonic monitoring thread
        motor.start()


        # Main thread will handle other tasks or just keep the program running
        while True:
            distance = ultrasonic.get_distance()
            if distance is not None:
                # print(f"Distance: {distance} m")
                controller.handle_ultrasonic(distance)
            else:
                print("Failed to get distance")
            time.sleep(0.03)
            pass  # Do nothing, just keep the main thread alive
    except KeyboardInterrupt:
        print("Exiting...")
        connection.exit()
        ultrasonic.exit()
        gyro.exit()
        motor.exit()
