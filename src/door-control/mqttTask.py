from mqtt_as import MQTTClient, config
import asyncio
from logging import Logging

class Mqtt:
  def __init__(self, clientId, server, port, user, password, topic, inboundQueue, outboundQueue, delaySeconds = 5): #topic is where the command for the door will be set
    self.config = config
    self.config["client_id"] = clientId
    self.config["server"] = server
    self.config["port"] = port
    self.topic = topic
    self.config["connect_coro"] = self.subscribe
    self.inboundQueue = inboundQueue
    self.outboundQueue = outboundQueue
    self.delay = delaySeconds
    self.config["user"] = user
    self.config["password"] = password
    self.config["subs_cb"] = self.callback
    self.client = MQTTClient(self.config)
  
  async def subscribe(self, client):
    await self.client.subscribe(self.topic, 1)
    
  async def connect(self):
    Logging.info("[MQTT] Attempting to connect to broker %s:%i" % (self.config["server"], self.config["port"]))
    await self.client.connect()
    Logging.info("[MQTT] Successfully connected to broker %s and subscribed to topic %s" % (self.config["server"], self.topic))

  def callback(self, topic, msg, retained):
    Logging.info("[MQTT] Received message on topic %s. Storing it in input queue." % (topic.decode()))
    self.inboundQueue.push({"topic": topic.decode(), "text": msg.decode()})
  
  async def processSendQueue(self):
    message = self.outboundQueue.popMessage()
    while message != None:
      Logging.info("[MQTT] Publishing message on topic %s" % message["topic"])
      await self.client.publish(message["topic"].encode(), message["text"].encode(), qos = 1)
      message = self.outboundQueue.popMessage()
  
  async def run(self): 
    await self.connect()
    while True:
      await asyncio.sleep(self.delay)
      try:
        await self.processSendQueue()
      except OSError as e:
        await self.connect()
        
    
  def publishMessage(self, topic, message):
    self.sendQueue.append({"topic": topic, "text": message})
  
  def isConnected(self):
    return self.client.isconnected()
  




