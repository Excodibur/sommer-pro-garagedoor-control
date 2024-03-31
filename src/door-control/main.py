import asyncio
from networkTask import Network
#from httpServerTask import HttpServer
from mqttTask import Mqtt
from queue import Queue
from doorControlTask import DoorControl
from logging import Logging
from storage import Storage
import json

def loadConfig():
  with open("config.json", "r") as f:
    return json.load(f)
 
async def main():
  config = loadConfig()
  Logging.loglevel = config["logging"]["level"]
  device = config["network"]["device"]
  inboundQueue = Queue()
  outboundQueue = Queue()
  
  try:
    storage = Storage(config["logfile"])
    Logging.extraLoggers.append(storage)
  except OSError:
    pass
  
  Logging.info("[MAIN] Starting")
  
  #tasks = [None] * 4
  tasks = [None] * 3
  nwTask = Network(config["network"]["ssid"], config["network"]["password"], config["network"]["device"])
  tasks[0] = asyncio.create_task(nwTask.checkConnection())
  mqttTask = Mqtt(config["mqtt"]["clientId"], config["mqtt"]["server"], config["mqtt"]["port"], config["mqtt"]["user"], config["mqtt"]["password"], f"{device}/command", inboundQueue, outboundQueue)
  tasks[1] = asyncio.create_task(mqttTask.run())
  doorControl = DoorControl(device, inboundQueue, outboundQueue)
  tasks[2] = asyncio.create_task(doorControl.monitorClosureState())
  statusCheck = { "wifi_status": nwTask.isConnected, "mqtt_status": mqttTask.isConnected, "door_closed": doorControl.isClosed}
  
  #HTTP Server is deactivated by default, since board reaches memory limit otherwise
  #httpsrvTask = HttpServer(nwTask, statusCheck)
  #tasks[3] = asyncio.create_task(httpsrvTask.run())
 
  Logging.info("[MAIN] Tasks are running")
  while True:
    await asyncio.sleep(0)

asyncio.run(main())
Logging.info("[MAIN] Finished")








