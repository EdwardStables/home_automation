import paho.mqtt.subscribe as mqtt

class mqtt_subscriber:
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.topics = None
        self.system_callback = None

    def set_data(self, topics, system_callback):
        self.topics = topics
        self.system_callback = system_callback

    def start(self):
        if self.topics == None or self.system_callback == None:
            raise Exception("Tried to start without initing topics or sys callbacks")
        mqtt.callback(self.callback_func, self.topics, hostname=self.hostname, port=self.port)

    def callback_func(self, client, userdata, message):
        self.system_callback(message.topic, message.payload)


    

