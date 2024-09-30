import connection
import motor
import ultrasonic

if __name__ == "__main__":
    try:
        # Start the status update thread
        connection.start()
        # Start the ultrasonic monitoring thread
        ultrasonic.start()

        # Main thread will handle other tasks or just keep the program running
        while True:
            pass  # Do nothing, just keep the main thread alive
    except KeyboardInterrupt:
        print("Exiting...")
        connection.exit()
        ultrasonic.exit()