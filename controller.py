from connection import publish_status
import motor
command_registry = {}

TURN_THRESHOLD = 50
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
    if motor.gear == 'P':
        return
    if (distance < TURN_THRESHOLD):
        if avoiding_obstacle == True:
            return

        publish_status(f"Obstacle detected! {int(distance)} cm")
        # motor.set_speed_internal(0)
        motor.stop_internal()
        # motor.set_speed_internal(50)
        motor.spin_right_internal()
        # handle_control_message({"command": "set_speed", "speed": 0})
        # handle_control_message({"command": "turn", "direction":"right"})
        avoiding_obstacle = True
    else:
        if avoiding_obstacle == False:
            return
        # handle_control_message({"command": "turn", "direction":"center"})
        publish_status("Obstacle cleared!")
        # motor.set_speed_internal(motor.speed)
        motor.back_to_center_internal()
        avoiding_obstacle = False


# Register commands
register_command("turn_angle", motor.turn)
register_command("spin", motor.spin)
register_command("set_gear", motor.set_gear)
register_command("set_speed", motor.set_speed)