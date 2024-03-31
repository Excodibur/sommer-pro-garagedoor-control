
import machine, os, sdcard
import re
import time

class Storage:
  cs = machine.Pin(16, machine.Pin.OUT)
  spi = machine.SPI(
    1
  )
  rootPath = "/sd"
  
  def __init__(self, config):
    self.file = config["name"]
    self.maxFiles = config["maxFiles"]
    self.maxFileSizeKb = config["maxFileSizeKb"]
    self.sd = sdcard.SDCard(Storage.spi, Storage.cs)
    os.mount(self.sd, Storage.rootPath)
  
  def write(self, message):
    try:
      st = os.stat(f"{Storage.rootPath}/{self.file}.current.log")
      fileSize = st[6]
      if fileSize > self.maxFileSizeKb * 1024:
        self.rotateFiles()
      #print(f"filetime: {st}")
    except OSError as error:
      print (error)
    file = open(f"{Storage.rootPath}/{self.file}.current.log", "a")
    file.write(f"{message}\n")
    file.close()
    
  def rotateFiles(self):
    print("Rotating logfile")
    curTime = time.localtime() 
    formatedTime = f"{curTime[0]}{curTime[1]:0>2}{curTime[2]:0>2}{curTime[3]:0>2}{curTime[4]:0>2}{curTime[5]:0>2}"
    oldFile = f"{Storage.rootPath}/{self.file}.current.log"
    newFile = f"{Storage.rootPath}/{self.file}.{formatedTime}.log"
    print(f"Renaming {oldFile} to {newFile}")
    os.rename(oldFile, newFile)
    
    self.cleanupOldFiles()
    
  def cleanupOldFiles(self):
    files = [f for f in os.listdir(Storage.rootPath) if re.match(f"^{self.file}\\.[\d]+\\.log$", f)]
    print(f"Files: {files}")
    if len(files) > self.maxFiles - 1:
      oldestFileTS = 99999999999999
      for file in files:
        timestamp = int(re.search(f"{self.file}\\.([\d]+)\\.log", file).group(1)) or 99999999999999
        if timestamp < oldestFileTS:
          oldestFileTS = timestamp
      oldestFile = f"{self.file}.{oldestFileTS}.log"
      print(f"oldest file is {oldestFile}. Removing it.")
      os.remove(f"{Storage.rootPath}/{oldestFile}")

