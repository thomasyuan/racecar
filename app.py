from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory

# Replace with your PubNub publish and subscribe keys
publish_key = 'pub-c-767218fd-fcf4-4285-83b5-69c03a17c076'
subscribe_key = 'sub-c-e6322d6f-8cd7-4ff1-a4f1-8605f88f4487'

pnconfig = PNConfiguration()
pnconfig.publish_key = publish_key
pnconfig.subscribe_key = subscribe_key
pnconfig.uuid = "car"

pubnub = PubNub(pnconfig)

class MySubscribeCallback(SubscribeCallback):
    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNConnectedCategory:
            print("Connected to PubNub")

    def message(self, pubnub, message):
        if (message.publisher != pnconfig.uuid):
            print(f"Received message: {message.message}")

    def presence(self, pubnub, presence):
        pass

pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels('my_channel').execute()

def publish_message(message):
    pubnub.publish().channel('my_channel').message(message).pn_async(my_publish_callback)

def my_publish_callback(envelope, status):
    if not status.is_error():
        print("Message published successfully")
    else:
        print("Failed to publish message")

if __name__ == "__main__":
    try:
        while True:
            message = input("Enter a message to publish: ")
            publish_message(message)
    except KeyboardInterrupt:
        print("Exiting...")
        pubnub.unsubscribe_all()
