import socket
import time
import threading

# A class to calculate the value of a function string
class FunctionCalculator:
  def evaluate(self, cmd):
    y = 0.
    print "exec \"%s\"" % cmd
    exec cmd
    print "y = %e" % y
    return y

# A class to calculate many the result of many equations at once. 
class SynchronousCalculator:
  def __init__(self):
    self.calculator =  FunctionCalculator()

  def evaluate(self, cmds):
    results=[]
    for cmd in cmds:
      results.append(self.calculator.evaluate(cmd))
    return results

# A class to hold the result from a BatchCalculatorThread
class StatusResult:
  cmd_status = 0
  result = 0.

  def __init__(self, status_val, result_val):
    self.cmd_status = status_val
    self.result = result_val

  def __str__(self):
    return "cmd_status: %d, result: %e" % (self.cmd_status, self.result)

  def __repr__(self):
    return "cmd_status: %d, result: %e" % (self.cmd_status, self.result)

# A threading class to interface with clients
class BatchCalculatorThread(threading.Thread):

  def __init__(self, sock):
    threading.Thread.__init__(self)
    self.sock = sock
    self.cmd = ''
    self.sr = StatusResult(0,0.) 
    self.processing = threading.Event()
    self.processing.clear()
    self.setDaemon(True)

  def run(self):
    while True:
      self.processing.wait() # block until a command is given
      print "Thread \"%s\" sending \"%s\"" % (self.getName(), self.cmd)
      self.sock.send(self.cmd)
      self.sr.result = float(self.sock.recv(1020))
      self.sr.cmd_status = 2 # finished 
      print "Thread \"%s\" recieved \"%s\"" % (self.getName(), self.sr.result)
      self.processing.clear() # ready for a new command
            
  def evaluate(self, cmd, sr):
    self.cmd = cmd
    self.sr = sr
    self.sr.cmd_status = 1 # processing
    self.processing.set()

  def processingCmd(self):
    return self.processing

  def cmd(self):
    return self.cmd

  def result(self):
    return self.result

# The BatchCalculator class, a master server class.
class BatchCalculator:
  def __init__(self,host,port):
    self.host = host
    self.port = port
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.settimeout(None) 
    self.client_sockets = []
    self.client_threads = []
    self.shutdown_flag = False
        
  def initialise(self):
    try:
      self.sock.bind((self.host, self.port))
    except socket.error:
      return
            
    self.sock.listen(5)
    self.server_thread = threading.Thread(target=self.serve_forever)
    self.server_thread.setDaemon(True)
    self.server_thread.start()
    print "Server running on %s and listening on %d" % (self.host, self.port)
        
  def serve_forever(self):
    while not self.shutdown_flag:
      print "Listening for a connection"
      try:
        request, client_address = self.sock.accept()
      except socket.error:
        return
      self.client_sockets.append(request)
      print "Received connection from ", client_address
            
      client_thread = BatchCalculatorThread(request)
      client_thread.start()
      self.client_threads.append(client_thread)
      print "Started an associated thread."
            
    if self.shutdown_flag == True:
      print "Listening socket shutting down"

  def disconnect(self):
    self.shutdown_flag = True # Stop listening 
    print "There are %s connections active" % len(self.client_sockets)

    while len(self.client_sockets) > 0: # Loop over clients
      sock = self.client_sockets.pop()
      print "Wrote DISCONNECT"
      sock.send("DISCONNECT") # Tell client to disconnect

  def shutdown(self):
    self.shutdown_flag = True # Stop listening
    self.sock.close()
    print "There are %s connections active" % len(self.client_sockets)

    while len(self.client_sockets) > 0: # Loop over clients
      sock = self.client_sockets.pop()
      print "Wrote EXIT"
      sock.send("EXIT") # Tell client to shutdown

# The Batch calculator client, which is to be deployed on a 
# remote compute node.
class BatchCalculatorClient(FunctionCalculator):
  def __init__(self, host, port):
    self.host = host
    self.port = port
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.connectionOpen = 0
    self.reconnectTime = 2
    self.rereadTime = 2

  def loop(self):
    while True:
      if self.connectionOpen == 0:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        HOST, PORT = self.host, int(self.port)
        try:
          # Connect to the server
          print "Connecting"
          self.sock.connect((HOST, PORT))
        except socket.error:
          self.sock.close()
          time.sleep(self.reconnectTime)
          print "Failed to connect"
          continue
        self.connectionOpen = 1
                
        # Read data from the server
        msg = self.sock.recv(1024)
        if msg is None:
          time.sleep(self.rereadTime)
          continue
            
        msg = msg.strip()
        if msg == "EXIT":
          break
            
        if msg == "DISCONNECT":
          self.sock.close()
          self.connectionOpen = 0
          time.sleep(self.reconnectTime)
          print "Disconnecting"
          continue

        result = "%e" % self.evaluate(msg)  
        self.sock.send(result)
