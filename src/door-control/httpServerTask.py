import asyncio
import re
from logging import Logging

class HttpServer:
  def loadPageFromTemplate(self, template, vars = None):
    templateDir = 'pages'
    with open(templateDir + '/' + template, 'r') as file:
      tmplBody = file.read()
    for key in vars:
      varValue = vars[key]
      
      #Check if varValue is a function or a normal value
      if callable(varValue):
        if key == "door_closed":
          value = "closed" if varValue() else "opened"
        else:
          value = "connected" if varValue() else "disconnected"
      else:
        value = varValue
        
      #Check if value is primitive type or list
      if type(value) is list:
        value = "<br/>\n".join(value)
      elif isinstance(value,int) or isinstance(value,float):
        value = str(value)
      
      Logging.debug("[HTTP] Replacing var: " + key + " with value: " + value)
      tmplBody = tmplBody.replace("{{"+key+"}}", value)

    Logging.debug("[HTTP] Rendering body: %s" % tmplBody)  
    return tmplBody
    
  def __init__(self, network, statusCheck, delaySeconds = 5):
    self.ROUTES = [
      {'path': '/', 'template': 'index.tpl', 'vars': {}},
      {'path': '/status', 'template': 'status.tpl', 'vars': statusCheck}, 
      {'path': '/style.css', 'template': 'style.css', 'vars': {}},
      {'path': '/logs', 'template': 'logs.tpl', 'vars': {"logNum": Logging.maxLogs, "logs": Logging.logs, "loglevel": Logging.loglevelName[Logging.loglevel]}}
    ]
    self.network = network
    self.delay = delaySeconds

  def getHeaders(self, request):
    headers = request.split('\r\n')
    parsedHeaders = {}
    parsedHeaders['path']   = re.search("^[A-Z]+\\s+(/[-a-zA-Z0-9_.]*)", headers[0]).group(1)
    parsedHeaders['method'] = re.search("^([A-Z]+)", headers[0]).group(1)
    i = 0
    for header in headers:
      if i == 0:
       i += 1
       continue
      splitHeader = header.split(' ')
      if len(splitHeader) < 2:
       continue
      headerName = splitHeader[0]
      headerValue = splitHeader[1]
      parsedHeaders[headerName] = headerValue
    return parsedHeaders
  
  def findRoute(self, request):
    headers = self.getHeaders(request)
    path = headers['path']
    Logging.debug("Path: "+path)
    for route in self.ROUTES:
      if route['path'] == path:
        return route
  
  def loadPage(self, request):
    route = self.findRoute(request)

    response = "";
    if route != None:
      data = self.loadPageFromTemplate(route['template'], route['vars'])
      response = {"headers": 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n', "data": data}
    else:
      response = {"headers": 'HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\nConnection: close\r\n'}
    
    return response
  
  async def handleClient(self, reader, writer):
    request = (await reader.read(1024))
    Logging.debug("REQUEST: %s" % (request))
    response = self.loadPage(request.decode('utf8'))
    
    headers = response["headers"]
    if "data" in response.keys():
      encodedResponseData = response["data"]
      encodedResponseLength = len(encodedResponseData)
      headers = headers + "Content-Length: %s" % (encodedResponseLength)
    else:
      encodedResponseData = ""
    
    fullResponse = "%s\r\n\r\n%s" % (headers, encodedResponseData)
    
    Logging.debug("[HTTP] RESPONSE: %s" % (fullResponse.encode('utf8')))
    writer.write(fullResponse.encode('utf8'))

    await writer.drain() 
    reader.close()
    await reader.wait_closed()
    writer.close()
    #await writer.wait_closed()
  
  async def run(self):
    Logging.info("[HTTP] Starting server")
    await asyncio.start_server(self.handleClient, "0.0.0.0", 80)
    while True:
      await asyncio.sleep(self.delay)





