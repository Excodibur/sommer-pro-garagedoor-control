import time

class Logging:
  logs = []
  loglevel = 3
  loglevelName = {1: "ERROR", 2: "WARN", 3: "INFO", 4: "DEBUG"}
  extraLoggers = []
  maxLogs = 100
  #loglevel = 1
  def info(message):
    Logging._log(3, message)
  
  def error(message):
    Logging._log(1, message)
    
  def warn(message):
    Logging._log(2, message)
    
  def debug(message):
    Logging._log(4, message)
    
  def _log(level, message):
    if level > Logging.loglevel:
      return
    if len(Logging.logs) >= Logging.maxLogs:
      Logging.logs.pop(0)
    curTime = time.localtime() 
    formatedMessage = f"{curTime[0]}-{curTime[1]:0>2}-{curTime[2]:0>2} {curTime[3]:0>2}:{curTime[4]:0>2}:{curTime[5]:0>2} [{Logging.loglevelName[level]}] {message}"
    #Logging.logs.append(formatedMessage)
    #Log to extra logger
    for logger in Logging.extraLoggers:
      logger.write(formatedMessage)
    print(formatedMessage)

