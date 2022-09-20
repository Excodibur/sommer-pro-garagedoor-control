#include <ArduinoMqttClient.h>
#include <ArduinoLog.h>
#include <ESP8266WiFi.h>
#include "arduino_config.h"

/*
   Author: Excodibur
   License: MIT

   Software for Lolin D1 mini pro based Garage door opener.
*/

#define PIN_SWITCH_S1 4 // 5 //OUTPUT: Door command - open
#define PIN_SWITCH_S2 5 // 4 //OUTPUT: Door command - close
#define PIN_SWITCH_S3 0 //INPUT: closure state

String wifiSsid = SECRET_SSID;
String wifiPass = SECRET_PASS;

String brokerHost = MQTT_BROKER_HOST;
int brokerPort = MQTT_BROKER_PORT;
String brokerUsername = MQTT_BROKER_USER;
String brokerPassword = MQTT_BROKER_PASSWORD;

String deviceName = DEVICE;

String topicDoorCommand = deviceName + "/command"; //INPUT: valid values: open/close
String topicDoorClosed  = deviceName + "/isclosed"; //OUTPUT: true (fully closed) / false (open/moving)

int delayBetweenRetriesMs = DELAY_BETWEEN_CONNECTION_RETRIES;

boolean doorIsClosed; //will be overwritten, but state should be managed in memory, instead of always updating topic

WiFiClient wifiClient;
MqttClient mqttClient(wifiClient);

void setup() {
  //Initialize serial and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  Log.begin(LOG_LEVEL, &Serial);

  // attempt to connect to Wifi network:
  connectWifi();

  Log.noticeln("Attempting to connect to the MQTT broker: %s", brokerHost);
  mqttClient.setUsernamePassword(brokerUsername, brokerPassword);
  connectMqtt();

  pinMode(PIN_SWITCH_S1, OUTPUT);
  digitalWrite(PIN_SWITCH_S1, LOW);
  pinMode(PIN_SWITCH_S2, OUTPUT);
  digitalWrite(PIN_SWITCH_S2, LOW);

  // Need to set INPUT PIN to HIGH (pullup) if switch is open, as it would be floating
  // if switch is closed (aka door closed), PIN will be grounded and LOW
  pinMode(PIN_SWITCH_S3, INPUT_PULLUP);

  checkDoorClosureState(true);

  // set the message receive callback
  mqttClient.onMessage(onMqttMessage);

  // Subscrite to IOBroker topics
  mqttClient.subscribe(topicDoorCommand);

  mqttClient.setKeepAliveInterval(2000);
}

void connectWifi() {
  Log.noticeln("Attempting to connect to SSID: %s", wifiSsid);

  while (WiFi.begin(wifiSsid, wifiPass) != WL_CONNECTED) {
    // failed, retry
    Log.warningln("Could not connect to Wifi network. Retrying...");
    delay(delayBetweenRetriesMs);
  }

  Log.noticeln("Successfully connected to the network");
}

void connectMqtt () {
  while (!mqttClient.connected()) {
    if (!mqttClient.connect(brokerHost.c_str(), brokerPort)) {
      // failed, retry again
      Log.warningln("MQTT connection failed! Error code %d. Retrying...", mqttClient.connectError());
    }
    delay(delayBetweenRetriesMs);
  }
  Log.noticeln("Succssfully connected to broker.");
}

void onMqttMessage(int messageSize) {
  String topic = mqttClient.messageTopic();
  String message = "";

  // use the Stream interface to print the contents
  while (mqttClient.available()) {
    message += (char)mqttClient.read();
  }

  Log.traceln("Received a message from topic '%s'. Message size: %d bytes. Message: %s", topic, messageSize, message);

  if (topic.equals(topicDoorCommand)) {
    if (message.equals("open")) {
      Log.noticeln("Opening door");
      setSwitchS1();
    } else if (message.equals("close")) {
      Log.noticeln("Closing door");
      setSwitchS2();
    } else
      Log.warningln("Received command '%s' on topic '%s', but ignoring it, as it is not supported.", message, topic);
  }
}

void setSwitchS1() {
  digitalWrite(PIN_SWITCH_S1, HIGH);
  delay(1000);
  digitalWrite(PIN_SWITCH_S1, LOW);
}

void setSwitchS2() {
  digitalWrite(PIN_SWITCH_S2, HIGH);
  delay(1000);
  digitalWrite(PIN_SWITCH_S2, LOW);
}

void checkDoorClosureState (bool overwriteState) {
  int closureState = digitalRead(PIN_SWITCH_S3);
  bool isClosed = (closureState == LOW) ? true : false;
  if ((isClosed != doorIsClosed) || (overwriteState)) {
    String newClosureState = (isClosed) ? "true" : "false";
    Log.noticeln("Door closure state changed to '%s'.", newClosureState);
    writeMqttMessageToTopic(topicDoorClosed, newClosureState);
    doorIsClosed = isClosed;
  }
}

void writeMqttMessageToTopic(String topic, String message) {
  Log.traceln("Writing new message '%s' to topic '%s'.", message, topic);
  mqttClient.beginMessage(topic);
  mqttClient.print(message);
  mqttClient.endMessage();
}

void loop() {
  if (!wifiClient.connected()) {
    Log.warningln("Network disconnected. Attempting to reconnect");
    connectWifi();
  }

  if (!mqttClient.connected()) {
    Log.warningln("Connected dropped. Attempting to reconnect");
    connectMqtt();
  }

  checkDoorClosureState(false);

  // call poll() regularly to allow the library to receive MQTT messages and
  // send MQTT keep alive which avoids being disconnected by the broker
  mqttClient.poll();
  
  Log.verboseln("Still running");
  delay(1000);
}
