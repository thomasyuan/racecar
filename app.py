from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
import time
from utils import get_serial  # Import the get_serial function

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
            # Handle control message here

    def presence(self, pubnub, presence):
        pass

pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels([public_channel, control_channel]).execute()

def publish_public_announcement():
    announcement = {"car_id": car_id, "status_channel": status_channel, "control_channel": control_channel}
    pubnub.publish().channel(public_channel).message(announcement).pn_async(my_publish_callback)

def publish_status(status_message):
    pubnub.publish().channel(status_channel).message({"status": status_message}).pn_async(my_publish_callback)

def publish_message(message):
    pubnub.publish().channel(control_channel).message(message).pn_async(my_publish_callback)

def my_publish_callback(envelope, status):
    if not status.is_error():
        print("Message published successfully")
    else:
        print("Failed to publish message")

if __name__ == "__main__":
    try:
        while True:
            # Send a status update every 10 seconds
            publish_status("ready")
            time.sleep(10)
    except KeyboardInterrupt:
        print("Exiting...")
        pubnub.unsubscribe_all()