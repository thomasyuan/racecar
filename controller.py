from time import sleep

command_registry = {}

TURN_THRESHOLD = 40

def register_command(command_name, handler):
    command_registry[command_name] = handler

def handle_control_message(message):
    command = message.get("command")
    if command in command_registry:
        handler = command_registry[command]
        handler(message)
    else:
        print(f"Unknown command: {command}")

def handle_ultrasonic(distance):
    print(f"Distance: {distance} cm")
    if (distance < TURN_THRESHOLD):
        print(f"Obstacle detected! {distance} cm")
        # Stop the car
        # handle_control_message({"command": "stop"})
        handle_control_message({"command": "turn", "direction":"right"})
    else:
        handle_control_message({"command": "turn", "direction":"center"})

def handle_gyro(gyro_x, gyro_y, gyro_z):
    print(f"Gyro X: {gyro_x}, Gyro Y: {gyro_y}, Gyro Z: {gyro_z}")

def handle_gps(data):
    print(f"GPS Data: {data}")

