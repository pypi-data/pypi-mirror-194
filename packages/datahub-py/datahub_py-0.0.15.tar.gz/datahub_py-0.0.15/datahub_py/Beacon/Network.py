import requests
import socket
import json
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm


class NetworkHelpers:
  def __init__(self):
    print("Network Helper")

  def get_local_ip_address(self):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 1))  # connect to a public IP address, any will do
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address

  def find_emitters_and_consumers(self):
    """Finds all Emitters and Consumers on the local network."""
    ip_address = self.get_local_ip_address()
    ip_prefix = '.'.join(ip_address.split('.')[:-1]) + '.'
    emitters_and_consumers = {}
    with ThreadPoolExecutor() as executor:
      futures = [executor.submit(self.find_on_ip, ip_prefix + str(i)) for i in range(256)]
      #futures = [executor.submit(self.find_on_ip, ip_address)]
      with tqdm(total=len(futures), desc='Scanning for Services', unit=' IP address') as pbar:
        for future in futures:
          devices = future.result()
          if devices is not None:
            for device in devices:
              emitters_and_consumers[device["id"]] = device
          pbar.update(1)
    print("Scanning completed")
    return emitters_and_consumers

  def get_rabbitmq_local_ip(self):
    """Gets the local IP address of the machine running RabbitMQ."""
    local_ip = self.get_local_ip_address()
    local_network_prefix = '.'.join(local_ip.split('.')[:-1]) + '.'
    port = 5672
    open_ips = []
    with ThreadPoolExecutor() as executor:
      futures = [executor.submit(self.check_port, local_network_prefix + str(i), port) for i in range(1, 255)]
      with tqdm(total=len(futures), desc='Scanning for RabbitMQ', unit=' IP address') as pbar:
        for future in futures:
          result = future.result()
          if result is not None:
            open_ips.append(result)
          pbar.update(1)
    if len(open_ips) == 0:
      return None
    print("Scanning completed")
    return open_ips[0]

  def check_port(self, ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((ip, port))
    #print("[DEBUG]", ip, port, result)
    sock.close()
    if result == 0:
      return ip
    return None
      


  def find_on_ip(self, address):
    """Gets the RabbitMQ queues and description of an Emitter or Consumer."""
    result = []
    for port in range(8000, 8011):
      try:
        response = requests.get(f'http://{address}:{port}/specs', timeout=0.1)
        if response.status_code == 200:
          data = json.loads(response.text)
          if 'queues' in data and 'description' in data:
            data['address'] = address
            data['port'] = port
            result.append(data)
      except:
        pass
    if len(result)==0:
      return None
    return result

  def get_available_port(self):
    """Finds an available port to use for the local server."""
    port = 8000
    while True:
      with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex(('localhost', port)) != 0:
          return port
      port += 1

    for p in open_ports:
      if p['port'] == 5672:
        return p['ip']

