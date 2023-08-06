from tinydb import TinyDB, Query, where
import pika
import json
import time
import requests
from .Network import NetworkHelpers
from flask import Flask, request
import threading


class Beacon:
  def __init__(self, project, config):
    print("Beacon Init")
    self.project = project
    self.config = config
    self.db = TinyDB(self.project.id+'.json')
    self.queues = {}
    self.devices = {}
    self.queueListeners = {}
    self.helper = NetworkHelpers()
    self.connection = None
    self.rabbitAutoconnect = False
    self.rabbitConnecting = False
    print("[Beacon] Setting up the routes...")
    self.setupServerRoutes()
  
  # Start the Beacon
  def start(self):
    self.initRabbit()
    self.pulseThread = threading.Thread(target=self.servicePulse, args=())
    self.pulseThread.start()
    print("[Beacon] Looking for devices on the local network...")
    self.findServices()
    self.displayServices()
    print("[Beacon] Saying hello...")
    self.sayHello()

  # Check the services pulse using a ping
  def servicePulse(self):
    while True:
      rmList = []
      for deviceID in self.devices.keys():
        if deviceID != self.project.id:
          response = self.callService(self.devices[deviceID], "/ping")
          if response is None or "id" not in response or response["id"] != deviceID:
            print("[Beacon] Device lost: ", self.devices[deviceID]["id"], self.devices[deviceID]["name"])
            rmList.append(deviceID)
      if len(rmList)>0:
        for deviceID in rmList:
            del self.devices[deviceID]
        rmList = []
      time.sleep(10)

  
  # Init the RabbitMQ connection
  def initRabbit(self):
    print("[Beacon] Scanning for RabbitMQ...")
    self.queueIP = self.helper.get_rabbitmq_local_ip()
    if self.queueIP is not None:
      print("[Beacon] RabbitMQ found on", self.queueIP)
      self.rabbitAutoconnect = False
      self.connectToRabbit()
    else:
      print("[Beacon] RabbitMQ not found")
      self.rabbitAutoconnect = True
    # Start the auto-connect thread
    self.serverThread = threading.Thread(target=self.rabbitAutoConnect, args=())
    self.serverThread.start()
  
  # Auto-connect to Rabbit if offline or disconnected (every 5 sec)
  def rabbitAutoConnect(self):
    while True:
      if self.rabbitAutoconnect and self.rabbitConnecting is not True:
        self.rabbitConnecting = True
        print("[Beacon] Scanning for RabbitMQ...")
        self.queueIP = self.helper.get_rabbitmq_local_ip()
        if self.queueIP is not None:
          self.rabbitAutoconnect = False
          self.connectToRabbit()
      time.sleep(5)

  # Connect to RabbitMQ
  def connectToRabbit(self):
    print("[Beacon] Connecting to RabbitMQ...")
    if self.queueIP is None:
      print("[Beacon] RabbitMQ not found")
      self.rabbitAutoconnect = True
    else:
      print("[Beacon] RabbitMQ found:", self.queueIP)
      print("[Beacon] Connecting...")
      try:
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.queueIP))
        print("[Beacon] RabbitMQ connected:", self.queueIP)
        self.rabbitConnecting = False
        # Upload the buffered data if any
        self.emitBufferedData()
      except Exception as e:
        self.onRabbitClose("connectToRabbit", e)
  
  # In case Rabbit closes
  def onRabbitClose(self):
    if self.rabbitAutoconnect is not True:
      print("[Beacon] RabbitMQ closed")
      self.rabbitAutoconnect = True
      self.queues = {} # Clears the queues
      self.connection = None # Reset RabbitMQ
  
  # Say hello to announce our presence to other devices
  def sayHello(self):
    for deviceID in self.devices.keys():
      if deviceID != self.project.id:
        response = self.callService(self.devices[deviceID], "/mesh/hello", self.project.specs()[0])
        #print("[Beacon] HELLO response: ", deviceID, response)
  
  # Execute a POST on one of the services
  def callService(self, device, endpoint, params=None, timeout=1):
    address = device["address"]
    port = device["port"]
    try:
      response = requests.post(f'http://{address}:{port}{endpoint}', data=params, timeout=timeout)
      #print("[Raw response]", f'http://{address}:{port}{endpoint}', response)
      if response.status_code == 200:
        data = json.loads(response.text)
        return data
    except:
      #print("[Raw response]", f'FAILED:: http://{address}:{port}{endpoint}')
      return None

  # Find all the online devices on the network
  def findServices(self):
    self.devices = self.helper.find_emitters_and_consumers()
  
  # Display the services that are online
  def displayServices(self):
    for deviceID in self.devices.keys():
      print("[Beacon]["+self.devices[deviceID]["name"]+":"+str(self.devices[deviceID]["id"])+"] port", self.devices[deviceID]["port"])
    return self.devices
  
  # Add a service to our list
  def addService(self, serviceData):
    if serviceData["id"] not in self.devices.keys():
      self.devices[serviceData["id"]] = serviceData
      print("[Beacon] New device: ", serviceData["id"], serviceData["name"])
      self.displayServices()
    
  # Setup the mandatory Beacon routes
  def setupServerRoutes(self):
    self.project.server.createRoute("/specs", self.project.specs)
    self.project.server.createRoute("/ping", self.ping)
    self.project.server.createRoute("/mesh/hello", self.newMeshService)
  
  # On ping
  def ping(self):
    return self.project.specs()

  # On new device
  def newMeshService(self):
    service = request.form.to_dict()
    print("[Mesh Data]", service)
    self.addService(service)
    return {"ok": True}, 200
  
  # Buffer data in a local db in case the queue is offline
  def bufferData(self, name, data):
    self.db.insert({'queue': name, 'data': data, "sent": False})
  
  # When RabbitMQ is back online, Emit buffered data
  def emitBufferedData(self):
    # Read the buffered data from TinyDB
    buffered_data = self.db.search(where('sent') == False)
    if len(buffered_data)>0:
      print("[Beacon] Starting upload of "+str(len(buffered_data))+" buffered items")
      # For each item in the buffered data
      doc_ids = []
      for item in buffered_data:
        queue_name = item['queue']
        data = item['data']
        # Emit the data
        self.emit(queue_name, data)
        doc_ids.append(item.doc_id)

        # Mark the data as sent
        #item['sent'] = True
        #self.db.update(item, doc_ids=[item.doc_id])

      self.db.remove(doc_ids=doc_ids)
      print("[Beacon] Buffer upload completed")
  
  # Emit data (public method)
  def emit(self, name, data, metas=None):
    if metas is None:
      metas = {}
    #print(name, data)
    data["serviceId"] = self.project.id
    self.pushQueue(name, data)

  # Push data to a queue (buffer if the queue is offline)
  def pushQueue(self, name, data):
    if self.connection is None:
      # No queue, we buffer
      #print("[Beacon:buffer]", name, data)
      self.bufferData(name, data)
    try:
      channel = self.getQueue(name)
      channel.basic_publish(exchange='', routing_key=name, body=json.dumps(data))
      #print("[Beacon:sent]", name, data)
    except Exception as e:
      self.onRabbitClose("pushQueue", e)
      print("[Beacon:buffer]", name, data)
      #self.bufferData(name, data)
  
  # Get an array of queues used by mesh services
  def getQueues(self):
    queues = []
    for deviceID in self.devices.keys():
      if "queues" in self.devices[deviceID].keys():
        for queue in self.devices[deviceID]["queues"]:
          queues.append(queue)
    return queues

  # Get a queue by name
  def getQueue(self, name):
    try:
      if name not in self.queues.keys():
        self.queues[name] = self.connection.channel()
        self.queues[name].queue_declare(queue=name, durable=True) #, passive=True
      return self.queues[name]
    except pika.exceptions.ConnectionWrongStateError as e:
      print("[PIKA:ConnectionWrongStateError]", e)
      return None
    except Exception as e:
      return None


  # Subscribe to a queue in a new thread
  # if name is "*", subscribe to all the queues
  def subscribe(self, name, callback):
    print("[subscribe]", name)
    if name == "*":
      queues = self.getQueues()
      print("[QUEUES]", queues)
      for queue in queues:
        self.subscribe(queue, callback)
    else:
      channel = self.getQueue(name)
      if channel is not None:
        self.pushQueue(name, {"ping": True})
        channel.basic_consume(queue=name, on_message_callback=callback)
        thread = threading.Thread(target=channel.start_consuming)
        thread.daemon = True
        thread.start()
      else:
        print("[Queue not found]", name)
  
  def onMessage(self, name, body):
    print("[onMessage]", name, body)
    if name in self.queueListeners:
      for cb in self.queueListeners[name]:
        print("[CB]", name, body)
        cb(name, body)
    if "*" in self.queueListeners:
      for cb in self.queueListeners["*"]:
        print("[CB]", name, body)
        cb(name, body)

  def listen(self, name):
    print("[listen]", name)
    if name == "*":
      queues = self.getQueues()
      print("[QUEUES]", queues)
      for queue in queues:
        self.listen(queue)
    else:
      try:
        channel = self.getQueue(name)
        if channel is not None:
          fw = lambda ch, method, properties, body: self.onMessage(name, body)
          channel.basic_consume(queue=name, on_message_callback=fw)
          thread = threading.Thread(target=channel.start_consuming)
          thread.daemon = True
          thread.start()
      except Exception as e:
        print("[SUBFAIL]", name, e)

  def onData(self, name, callback):
    if name not in self.queueListeners:
      self.queueListeners[name] = []
    self.queueListeners[name].append(callback)
