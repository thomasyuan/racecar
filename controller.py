from connection import publish_status
import motor

command_registry = {}

TURN_THRESHOLD = 40
avoiding_obstacle = False

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
    # print(f"Distance: {distance} cm")
    global avoiding_obstacle
    if (distance < TURN_THRESHOLD):
        if avoiding_obstacle == True:
            return

        publish_status(f"Obstacle detected! {distance} cm")
        # motor.set_speed_internal(0)
        publish_status("turning right")
        motor.turn_right_internal()
        # handle_control_message({"command": "set_speed", "speed": 0})

        # handle_control_message({"command": "turn", "direction":"right"})
        avoiding_obstacle = True
    else:
        if avoiding_obstacle == False:
            return
        # handle_control_message({"command": "turn", "direction":"center"})
        publish_status("Obstacle cleared!")
        motor.back_to_center_internal()
        avoiding_obstacle = False

def handle_gyro(gyro_x, gyro_y, gyro_z):
    print(f"Gyro X: {gyro_x}, Gyro Y: {gyro_y}, Gyro Z: {gyro_z}")

