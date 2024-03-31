import network
import asyncio
import ntptime
import time
from logging import Logging
from led import Led

class Network:
  def __init__(self, ssid, password, hostname, delaySeconds = 2):
    self.ssid = ssid
    self.password = password
    self.hostname = hostname
    self.delay = delaySeconds
    self.sta_if = network.WLAN(network.STA_IF)
    #Setting hostname does not yet work on esp8266
    # https://github.com/micropython/micropython/issues/11450
    # https://github.com/micropython/micropython/issues/5475
    network.hostname(hostname)
  
  async def checkConnection(self):
    while True:
      Logging.debug("[NETW] Checking connection")
      if not self.sta_if.isconnected():
        self.connect()
      await asyncio.sleep(self.delay)
    
  def connect(self):
    Logging.info('[NETW] connecting to network...')
    self.sta_if.active(True)
    self.sta_if.connect(self.ssid, self.password)
    while not self.sta_if.isconnected():
      Logging.debug("[NETW] Attempting to connect")
      Led.blink()
      time.sleep(self.delay)
    
    Logging.info(f"[NETW] network config:{self.sta_if.ifconfig()}")
    self.setTime()
            
  def isConnected(self):
    Logging.debug("[NETW] checking if connected. Result: %d" % self.sta_if.isconnected())
    return self.sta_if.isconnected()
    
  def setTime(self):
    Logging.debug("[NETW] Updating local time from internet")
    ntptime.settime()






