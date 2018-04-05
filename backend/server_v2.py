import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
import sys
import json
import base64
from server_api import *

# Socket with host defines
SOCKET        = "SOCKET"

# Server defines
PORT          = 8080

# Communication protocol defines
WRITE_DATA    = "WRITE_DATA"
READ_DATA     = "READ_DATA"
GET_IMAGE     = "GET_IMAGE"

# Error Messages
INVALID_DATA  = "The client sent invalid data"

sock = None

class WSHandler(tornado.websocket.WebSocketHandler):
  sock = None

  def open(self):
    print('new connection')

  def on_message(self, message):
    msg = json.loads(message)
    response = {}
    print(message)
    header = msg['type']
    payload = msg['payload']

    result = handle_request(header, payload)

    self.write_message(result)

  def on_close(self):
    print('Connection closed')

  def check_origin(self, origin):
    return True

class GetRequestHandler(tornado.web.RequestHandler):
  def set_default_headers(self):
    self.set_header("Access-Control-Allow-Origin", "*")
    self.set_header("Access-Control-Allow-Headers", "x-requested-with")
    self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

  def get(self):
    header = self.get_query_argument("type", None)
    payload = json.loads(self.get_query_argument("data", None))

    print(header)
    print(payload)
    result = handle_request(header, payload)
    
    self.write(result)

"""
MAIN APPLICATION
"""
def main():
  # Opening socket with host
  global sock

  sock = get_socket()

  application = tornado.web.Application([
    (r'/ws', WSHandler),
    (r'/hw', GetRequestHandler),
  ])

  # Configuring the http server
  http_server = tornado.httpserver.HTTPServer(application)
  http_server.listen(PORT)

  # Setting IP
  myIP = socket.gethostbyname(socket.gethostname())
  print('*** Websocket Server Started at %s***' % myIP)
  
  # Starting webserver
  tornado.ioloop.IOLoop.instance().start()

def get_socket():
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server_address = (SOCKET)
    sock.connect(server_address)

    return sock

def handle_request(header, payload):
  if header == WRITE_DATA:
    response = write_data_handler(sock, header, payload, False)
  elif header == READ_DATA:
    response = read_data_handler(sock, header, False)
  elif header == GET_IMAGE:
    response = get_image(sock, header, payload)
  elif header:
    response = socket_send_command(sock, header)
  else:
    response = INVALID_DATA

  return {'type' : header, 'data': response}

if __name__ == "__main__":
  main()