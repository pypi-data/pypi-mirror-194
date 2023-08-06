__version__ = '0.0.15'

print("Datahub Version :: ", __version__)

from .Project import Project
from .Beacon import Beacon
from .Beacon.Network import NetworkHelpers as Network
from .CTRL import Server

def hello_world():
    print("This is my first pip package!")
