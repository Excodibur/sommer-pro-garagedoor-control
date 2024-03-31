import time
from machine import Pin

class Led:
  pLed = Pin(2, Pin.OUT)
  
  def blink(duration = 0.5):
    Led.pLed.value(0)
    time.sleep(duration)
    Led.pLed.value(1)
    

