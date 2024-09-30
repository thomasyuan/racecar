import time
import controller  # Import the command handler module

from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from utils import get_serial  # Import the get_serial function
from utils import start_daemon_thread  # Import the start_daemon_thread function

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

class MySubscribeCallback(SubscribeCallback):
    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNConnectedCategory:
            print("Connected to PubNub")
            # Announce presence on the public channel
            publish_public_announcement()

    def message(self, pubnub, message):
        if message.channel == control_channel:
            print(f"Received control message: {message.message}")
            controller.handle_control_message(message.message)

    def presence(self, pubnub, presence):
        pass

pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels([public_channel, control_channel]).execute()

def publish_public_announcement():
    announcement = {"car_id": car_id, "status_channel": status_channel, "control_channel": control_channel}
    pubnub.publish().channel(public_channel).message(announcement).pn_async(lambda envelope, status: my_publish_callback(envelope, status, announcement))

def publish_status(status_message):
    message = {"status": status_message}
    pubnub.publish().channel(status_channel).message(message).pn_async(lambda envelope, status: my_publish_callback(envelope, status, message))

def publish_message(message):
    pubnub.publish().channel(control_channel).message(message).pn_async(lambda envelope, status: my_publish_callback(envelope, status, message))

def my_publish_callback(envelope, status, message):
    if not status.is_error():
        print(f"Message published successfully: {message}")
    else:
        print(f"Failed to publish message: {message}")

def send_status_updates():
    while True:
        publish_status("alive")
        time.sleep(10)

def start():
    start_daemon_thread(send_status_updates)

def main():
    start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Exiting...")
        pubnub.unsubscribe_all()

if __name__ == "__main__":
    main()