from ..Beacon import Beacon
from ..CTRL import Server

import random
import string

class Project:
  def __init__(self, config):
    print("Project Init")
    self.config = config
    self.id = self.generateID()
    print("[Project] ID: "+self.id)
    self.server = Server(self, self.config)
    self.beacon = Beacon(self, self.config)
    self.port = self.beacon.helper.get_available_port()
  
  def start(self):
    self.server.start(self.port)
    self.beacon.start()
  
  def generateID(self):
    return self.config.ProjectSpecs["type"]+(''.join(random.choices(string.ascii_uppercase + string.digits, k=7)))

  # Mandatory endpoint
  def specs(self):
    return {
      "id": self.id,
      "name": self.config.ProjectSpecs["name"],
      "queues": self.config.ProjectSpecs["queues"],
      "description": self.config.ProjectSpecs["description"],
      "address": self.beacon.helper.get_local_ip_address(),
      "port": self.port
    }, 200
