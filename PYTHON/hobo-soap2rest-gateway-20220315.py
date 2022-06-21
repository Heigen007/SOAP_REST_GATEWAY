# PYTHON 3.3.5

# VERSION FROM 15.03.2022 23:50

from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from getStockList import getStockList
from getRequest import getRequest
from getMaterialInStock import getMaterialInStock
# import datetime


def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
  server_address = ('', 8000)
  httpd = server_class(server_address, handler_class)
  print("Server started on port 8000")
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    httpd.server_close()


class HttpGetHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/api/hobo-bff/v0.5/MMMS_Stock":
            getStockList(self)
        elif self.path == "/api/hobo-bff/v0.5/MMMS_Request":
            getRequest(self)
        elif self.path == "/api/hobo-bff/v0.5/MMMS_Material_In_Stock":
            getMaterialInStock(self)

run(handler_class=HttpGetHandler)