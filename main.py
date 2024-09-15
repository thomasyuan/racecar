import time
import RPi.GPIO as GPIO
from camera import initialize_camera, capture_image, process_image
from ultrasonic import initialize_ultrasonic, read_ultrasonic_sensor
from motor import initialize_motor, control_motor

def main():
    # Initialize modules
    camera = initialize_camera()
    initialize_ultrasonic()
    initialize_motor()

    try:
        while True:
            image = capture_image(camera)
            if image is not None:
                process_image(image)

            distance = read_ultrasonic_sensor()
            if distance < 30:  # Example threshold for obstacle detection
                control_motor('stop')
            else:
                control_motor('move')

            time.sleep(0.1)  # Adjust the loop delay as needed

    except KeyboardInterrupt:
        print("Program stopped by user")

    finally:
        camera.release()
        GPIO.cleanup()

if __name__ == "__main__":
    main()