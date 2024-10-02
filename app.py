import connection
import motor
import gyro
import ultrasonic

if __name__ == "__main__":
    try:
        # Start the status update thread
        connection.start()
        # Start the ultrasonic monitoring thread
        motor.start()


        ultrasonic.monitor_ultrasonic(0.03)
        # Main thread will handle other tasks or just keep the program running
        # while True:
        #     pass  # Do nothing, just keep the main thread alive
    except KeyboardInterrupt:
        print("Exiting...")
        connection.exit()
        ultrasonic.exit()
        gyro.exit()
        motor.exit()
