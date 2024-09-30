command_registry = {}

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

def handle_gyro(data):
    gyro_x = data.get("gyro_x")
    gyro_y = data.get("gyro_y")
    gyro_z = data.get("gyro_z")
    print(f"Gyro X: {gyro_x}, Gyro Y: {gyro_y}, Gyro Z: {gyro_z}")

def handle_gps(data):
    print(f"GPS Data: {data}")

