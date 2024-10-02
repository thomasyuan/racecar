import json
import time
import threading

from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from utils import get_serial
from utils import start_daemon_thread
from datetime import datetime

publish_key = 'pub-c-767218fd-fcf4-4285-83b5-69c03a17c076'
subscribe_key = 'sub-c-e6322d6f-8cd7-4ff1-a4f1-8605f88f4487'

car_id = get_serial()  # Unique identifier for the car
public_channel = "car_public"
control_channel = f"car_control_{car_id}"
status_channel = f"car_status_{car_id}"

pnconfig = PNConfiguration()
pnconfig.publish_key = publish_key
pnconfig.subscribe_key = subscribe_key
pnconfig.uuid = car_id

pubnub = PubNub(pnconfig)

# Create a stop event
stop_event = threading.Event()

class MySubscribeCallback(SubscribeCallback):
    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNConnectedCategory:
            print("Connected to PubNub")
            # Announce presence on the public channel
            publish_public_announcement()

    def message(self, pubnub, message):
        from controller import handle_control_message  # Local import to avoid circular dependency

        if message.channel == control_channel:
            publish_status(f"Received control message: {message.message}")
            if isinstance(message.message, dict):
                handle_control_message(message.message)
            else:
                try:
                    # Attempt to parse the message as JSON
                    parsed_message = json.loads(message.message)
                    handle_control_message(parsed_message)
                except json.JSONDecodeError:
                    print("Received invalid JSON message")
        elif message.channel == public_channel:
            print(f"Received public message: {message.message}")
            if isinstance(message.message, dict):
                if message.message.get("query") == "online_cars":
                    publish_public_announcement()
            else:
                try:
                    # Attempt to parse the message as JSON
                    parsed_message = json.loads(message.message)
                    if parsed_message.get("query") == "online_cars":
                        publish_public_announcement()
                except json.JSONDecodeError:
                    print("Received invalid JSON message")

    def presence(self, pubnub, presence):
        pass

pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels([public_channel, control_channel]).execute()

def publish_public_announcement():
    announcement = {"car_id": car_id, "status_channel": status_channel, "control_channel": control_channel}
    pubnub.publish().channel(public_channel).message(announcement).pn_async(lambda envelope, status: my_publish_callback(envelope, status, announcement))

# def publish_status(status_message):
#     message = {"status": status_message}
#     pubnub.publish().channel(status_channel).message(message).pn_async(lambda envelope, status: my_publish_callback(envelope, status, message))

def publish_status(message):
    timestamp = datetime.now().strftime("%H:%M:%S:%f")[:-3]  # Format as hh:mm:ss:ms
    status_message = {"status": f"{timestamp} {message}"}
    pubnub.publish().channel(status_channel).message(status_message).pn_async(lambda envelope, status: my_publish_callback(envelope, status, message))

def my_publish_callback(envelope, status, message):
    if not status.is_error():
        print(f"Message published successfully: {message}")
    else:
        print(f"Failed to publish message: {message}")

def send_status_updates():
    while not stop_event.is_set():
        publish_status("alive")
        time.sleep(3)

def start():
    stop_event.clear()
    start_daemon_thread(send_status_updates)

def exit():
    stop_event.set()
    pubnub.unsubscribe_all()

def main():
    try:
        send_status_updates()
    except KeyboardInterrupt:
        print("Exiting...")
        pubnub.unsubscribe_all()

if __name__ == "__main__":
    main()