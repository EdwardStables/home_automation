import paho.mqtt.client as mqtt
from time import sleep

class mqtt_subscriber:
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.topics = None
        self.system_callback = None
        self.mqtt_client = mqtt.Client()
        self.is_connected = False

    def set_data(self, topics, system_callback):
        self.topics = topics
        self.system_callback = system_callback

    def start(self):
        if self.topics == None or self.system_callback == None:
            raise Exception("Tried to start without initing topics or sys callbacks")
        #mqtt.callback(self.callback_func, self.topics, hostname=self.hostname, port=self.port)

        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_disconnect = self.on_disconnect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.on_subscribe = self.on_subscribe

        self.mqtt_client.connect_async(self.hostname, self.port)
        self.mqtt_client.loop_start()

        while self.is_connected is False:
            sleep(0.1)

        qos = 2
        result, mid = self.mqtt_client.subscribe([(t, qos) for t in self.topics])
        print(f"subscribe request result: {result}")
        print(f"subscribe request mids: {mid}")

    def on_subscribe(self, client, userdata, mid, granted_qos):
        print(f"Got subscription callback, mids: {mid}")

    def on_message(self, client, userdata, message):
        self.system_callback(message.topic, message.payload)

    def on_connect(self, client, userdata, flags, rc):
        self.is_connected = True
        print(f"Connected successfully to client: {client}")

    def on_disconnect(self, client, userdata, flags, rc):
        self.is_connected = False
        print(f"Disconnected from client")


    

