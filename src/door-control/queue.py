class Queue:
  def __init__(self):
    self.queue = []
  
  def push(self, message):
    self.queue.append(message)
  
  def getQueue(self):
    return self.queue
    
  def popMessage(self):
    message = None
    if len(self.queue) > 0:
      message = self.queue[0]
      self.queue.pop(0)
    return message

