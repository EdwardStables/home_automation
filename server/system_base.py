# Base classes for setting up systems that can be automated
from threading import Timer
import json

class System:
    def __init__(self, name, mqtt, topic_callbacks):
        self.name = name
        self.mqtt = mqtt
        self.topic_callbacks = topic_callbacks

        if "test" not in self.topic_callbacks:
            self.topic_callbacks["test"] = self.echo_message


        self.mqtt.set_data(
            ['/'.join([self.name, t]) for t in self.topic_callbacks.keys()], 
            self.rx
        )
        self.mqtt.start()
        print(f"Starting MQTT listing for system {self.name} with topics:")
        for t in self.mqtt.topics:
            print(t)

    def echo_message(self, message):
        print(f"Echoed message: {message}")
    
    def rx(self, topic, message):
        topic = '/'.join(topic.split('/')[1:])
        message = json.loads(message)
        target = self.topic_callbacks.get(topic, self.echo_message)
        target(message)
class Coffee(System):
    def __init__(self, mqtt):
        super().__init__(
            "coffee",
            mqtt,
            {
                "start_timer"   : self.start_timer,
                "reset_timer"   : self.reset_timer,
                "pause_timer"   : self.pause_timer,
                "unpause_timer" : self.unpause_timer,
            },
        )

        #state can be IDLE, COUNTING, or PAUSED
        self.state = "IDLE"
        self.time = 0

    def count(self):
        print(f"Coffee counter is {self.state}, time is {self.time}")
        if self.state == "COUNTING":
            self.time -= 1

            if self.time <= 0:
                self.state = "IDLE"

            self.schedule_count()

        elif self.state == "IDLE":
            self.time = 0
        elif "PAUSED":
            pass

    def schedule_count(self):
        Timer(1, self.count).start()

    def start_timer(self, message):
        """Overwrite current time"""
        self.state = "COUNTING"
        self.time = message["time"]
        self.schedule_count()

    def reset_timer(self, message):
        self.state = "IDLE"
        self.time = 0

    def pause_timer(self, message):
        self.state = "PAUSED"

    def unpause_timer(self, message):
        self.state = "COUNTING"
        self.schedule_count()
