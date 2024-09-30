from controller import register_command

def turn_right(message):
    degree = message.get("degree", 0)
    print(f"Turning right by {degree} degrees")
    # Implement the logic to turn the car right by the specified degree

def turn_left(message):
    degree = message.get("degree", 0)
    print(f"Turning left by {degree} degrees")
    # Implement the logic to turn the car left by the specified degree

def set_speed(message):
    speed = message.get("speed", 0)
    print(f"Setting speed to {speed}")
    # Implement the logic to set the car's speed

# Register commands
register_command("turn_right", turn_right)
register_command("turn_left", turn_left)
register_command("set_speed", set_speed)