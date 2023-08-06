from flask import Flask, request
from flask_restful import Api
from werkzeug.serving import make_server
import threading

class Server:
  def __init__(self, project, config):
    self.config = config
    self.project = project
    self.app = Flask(__name__)
    self.api = Api(self.app)
    self.routes = {}
  
  def createRoute(self, path, callback):
    self.routes[path] = callback
  
  def handle_request(self, path=None):
    if path is None:
      path = request.path
    else:
      path = "/"+path
    if path not in self.routes:
      return {"error": True}, 404
    return self.routes[path]()
  
  def start(self, port):
    self.app.add_url_rule('/', 'handle_request', self.handle_request, methods=['GET', 'POST'])
    self.app.add_url_rule('/<path:path>', 'handle_request', self.handle_request, methods=['GET', 'POST'])
    self.server = make_server('0.0.0.0', port, self.app)

    self.serverThread = threading.Thread(target=self.server.serve_forever, args=())
    self.serverThread.start()
    print("[Server] Started on port", port)
    
  def stop(self):
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
      raise RuntimeError('Not running with the Werkzeug Server')
    func()


"""
def index():
  return {"hello": "world"}, 200

server = Server({}, {})
server.createRoute("/", index)
server.start(8000)
"""