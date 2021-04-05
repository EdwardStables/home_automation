#include "secrets.h"
#include <WiFi101.h>
#include <MQTT.h>

const char ssid[] = SECRET_SSID;
const char pass[] = SECRET_PASS;
const char hostname[] = MQTT_HOST;
const int16_t port = 1887;

const int GREEN_LED_PIN = 9;
const int RED_LED_PIN = 10;
const int BUTTON1_PIN = 12;
const int BUTTON2_PIN = 11;


WiFiClient net;
MQTTClient client;

unsigned long last_button1_millis = 0;
unsigned long last_button2_millis = 0;

void connect() {
  Serial.print("checking wifi...");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(1000);
  }

  Serial.print("\nconnecting...");
  while (!client.connect("arduino", "public", "public")) {
    Serial.print(".");
    delay(1000);
  }

  Serial.println("\nconnected!");

  client.subscribe("light/green");
  client.subscribe("light/red");
}

void messageReceived(String &topic, String &payload) {
  Serial.println("incoming: " + topic + " - " + payload);    
  int local_pin = 0;
  if (topic == "light/green")
      local_pin = GREEN_LED_PIN;
  else if (topic == "light/red")
      local_pin = RED_LED_PIN;
    
  if (local_pin != 0)
    if (payload == "on")
        digitalWrite(local_pin, HIGH);
    else if (payload == "off")
        digitalWrite(local_pin, LOW);

}

void setup() {
  Serial.begin(115200);
  WiFi.setPins(8,7,4,2);
  WiFi.begin(ssid, pass);

  pinMode(GREEN_LED_PIN, OUTPUT);
  pinMode(RED_LED_PIN, OUTPUT);
  pinMode(BUTTON1_PIN, INPUT);
  pinMode(BUTTON2_PIN, INPUT);

  digitalWrite(GREEN_LED_PIN, LOW);
  digitalWrite(RED_LED_PIN, LOW);

  client.begin(hostname, net);
  client.onMessage(messageReceived);

  connect();
}

int button1_state;
int button2_state;

void loop() {
  client.loop();

  if (!client.connected()) {
    connect();
  }

  button1_state = digitalRead(BUTTON1_PIN);
  button2_state = digitalRead(BUTTON2_PIN);

  if ( button1_state == HIGH && millis() - last_button1_millis > 1000) {
   last_button1_millis = millis();
   client.publish("coffee/test", "button_1_pressed");
   Serial.println("1 pressed\n");
  }


  if (button2_state == HIGH && millis() - last_button2_millis > 1000) {
    last_button2_millis = millis();

    client.publish("coffee/test", "button_2_pressed");
    Serial.println("2 pressed\n");
  }

}