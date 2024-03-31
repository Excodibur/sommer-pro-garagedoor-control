import asyncio
import time
from machine import Pin
from logging import Logging

class DoorControl:
  pClosureState = Pin(0, Pin.IN)
  pOpenDoorCmd  = Pin(5, Pin.OUT)
  pCloseDoorCmd = Pin(4, Pin.OUT)
  
  def __init__(self, deviceName, inboundQueue, outboundQueue, aliveIntervalSeconds, delaySeconds = 5):
    self.doorClosed = False
    self.delay = delaySeconds
    self.deviceName = deviceName
    self.inboundQueue = inboundQueue
    self.outboundQueue = outboundQueue
    self.aliveIntervalSeconds = aliveIntervalSeconds
    self.lastAliveTS = 0
    
  def openDoor(self):
    self.pOpenDoorCmd.value(1)
    time.sleep(1)
    self.pOpenDoorCmd.value(0)
    
  def closeDoor(self):
    self.pCloseDoorCmd.value(1)
    self.pCloseDoorCmd.value(1)
    time.sleep(1)
    self.pCloseDoorCmd.value(0)
    
  def processInboundQueue(self):
    message = self.inboundQueue.popMessage()
    while message != None:
      Logging.info("[DOOR] Action triggerd. %s door" % (message["text"]))
      if (message["text"] == "open"):
        self.openDoor()
      else:
        self.closeDoor()
      message = self.inboundQueue.popMessage()

  def checkClosureState(self, overwrite = False):
    closureState = self.pClosureState.value()
    isClosed = True if closureState == 0 else False
    if ((isClosed != self.doorClosed) or overwrite):
      newState = "true" if isClosed else "false"
      Logging.info("[DOOR] Closure state changed to %s" % newState)
      self.doorClosed = isClosed
      self.outboundQueue.push({"topic": self.deviceName + "/isClosed", "text": newState})
  
  def updateAliveTimestamp(self):
    currentTime = time.time()
    formatedTime = time.localtime()
    if currentTime - self.aliveIntervalSeconds > self.lastAliveTS:
      self.outboundQueue.push({"topic": self.deviceName + "/lastUpdate", "text": f"{formatedTime[0]}-{formatedTime[1]:0>2}-{formatedTime[2]:0>2} {formatedTime[3]:0>2}:{formatedTime[4]:0>2}:{formatedTime[5]:0>2}"})
      self.lastAliveTS = currentTime
  
  async def monitorClosureState(self):
    self.checkClosureState(True)
    while (True):
      self.checkClosureState()
      self.processInboundQueue()
      self.updateAliveTimestamp()
      await asyncio.sleep(self.delay)

  def isClosed(self):
    return self.doorClosed



