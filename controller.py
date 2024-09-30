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

def handle_ultasonic(distance):
    print(f"Distance: {distance} cm")

def handle_imu(data):
    print(f"IMU Data: {data}")

def handle_gps(data):
    print(f"GPS Data: {data}")

