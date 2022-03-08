from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import xml.etree.ElementTree as ET
import requests
import datetime


headers = {'AUTHORIZATION': '123'}
globalTimeout = 20


def ifnull(var):
    if var is None: return str(var)
    return var


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


def getStockList(self):
    try:
        url = 'http://10.8.4.244:8010/api/material-movement/v1.0/stock'
        try:
            r = requests.get(url, headers=headers, timeout=globalTimeout)
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout):
            return generateErrorXml(self, "Сервер СУДМ 10.8.4.244:8010 не ответил на вызов GET /api/material-movement/v1.0/stock в течение " + str(globalTimeout) + " секунд",  False, 0)
        except Exception as e:
            return generateErrorXml(self, "Ошибка при вызове GET /api/material-movement/v1.0/stock (Сервер СУДМ 10.8.4.244:8010): " + str(e), False, 0)

        json = r.json()

        if('stocks' not in json):
            return generateErrorXml(self, "От сервера СУДМ 10.8.4.244:8010 на вызов GET /api/material-movement/v1.0/stock получен неожиданный ответ:", True, r.status_code)
        elif(json['stocks'] == []):
            return generateErrorXml(self, "От сервера СУДМ 10.8.4.244:8010 на вызов GET-метода /api/material-movement/v1.0/stock получен пустой список складов")

        xml = "<soapenv:Envelope"
        xml += "xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\""
        xml += "xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\""
        xml += "xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">"
        xml += "<soapenv:Body>"
        xml += "<ns0:GetListResponse"
        xml += "xmlns:ns0=\"urn:MMMS_Stock\""
        xml += "xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\""
        xml += "xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">"
        for item in json['stocks']:
            xml += "<ns0:v>"
            xml += "<ns0:id>" + str(item['id']) + "</ns0:id>"
            xml += "<ns0:name>" + ifnull(item['name']) + "</ns0:name>"
            xml += "</ns0:v>"
        xml += "</ns0:GetListResponse>"
        xml += "</soapenv:Body>"
        xml += "</soapenv:Envelope>"


        self.send_response(200)
        self.send_header("Content-type", "application/xml")
        self.end_headers()
        self.wfile.write(xml.encode())
    except Exception as e:
        return generateErrorXml(self, "Cистемная ошибка в коде реализации сервиса /api/hobo-bff/v0.5/MMMS_Stock.GetList: " + str(e), False, 0)


def getRequest(self):
    try:
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)
        myroot = ET.fromstring(post_body)
        tmp = myroot[0][0][0].text
        if myroot[0][0].tag.split("}")[1] == "GetList":
            getRequestGetList(self, tmp)
        if myroot[0][0].tag.split("}")[1] == "Get":
            getRequestGet(self, tmp)
    except Exception as e:
        return generateErrorXml(self, "Cистемная ошибка в коде реализации сервиса /api/hobo-bff/v0.5/MMMS_Request: " + str(e), False, 0)


def getRequestGetList(self, id):
    try:
        url = 'http://10.8.4.244:8010/api/material-movement/v1.0/material-movement-request?stockId=' + id + '&dateFrom=2022-01-01T00:00:00+06:00'
        try:
            r = requests.get(url, headers=headers, timeout=globalTimeout)
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout):
            return generateErrorXml(self, "Сервер СУДМ 10.8.4.244:8010 не ответил на вызов GET /api/material-movement/v1.0/material-movement-request в течение " + str(globalTimeout) + " секунд",  False, 0)
        except Exception as e:
            return generateErrorXml(self, "Ошибка при вызове GET /api/material-movement/v1.0/material-movement-request (Сервер СУДМ 10.8.4.244:8010): " + str(e), False, 0)

        json = r.json()
        xml= "<s:Envelope"
        xml+= "xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\""
        xml+= "xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\""
        xml+= "xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">"
        xml+= "<s:Body>"
        xml+= "<n:GetListResponse"
        xml+= "xmlns:n=\"urn:MMMS_Request\""
        xml+= "xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\""
        xml+= "xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">"
        for item in json['materialMovementRequests']:
            t = item['createDate']
            hours_added = datetime.timedelta(hours = int(t.split("+")[1].split(":")[0]) - 6, minutes = int(t.split("+")[1].split(":")[1]))
            dateTime = datetime.datetime(int(t.split('-')[0]), int(t.split('-')[1]), int(t.split('T')[0].split('-')[2]), int(t.split('T')[1].split(':')[0]), int(t.split(':')[1]), int(t.split(':')[2].split('.')[0]))
            dateTime -= hours_added
            xml += "<n:v>"
            xml += "<n:id>" + str(item['id']) + "</n:id>"
            xml += "<n:stateName>" + str(item['stateId']) + "</n:stateName>"
            xml += "<n:senderStockName>" + str(item['senderStockId']) + "</n:senderStockName>"
            xml += "<n:stateUpdateDate>" + str(item['createDate']) + "</n:stateUpdateDate>"
            xml += "<n:stateName_and_updateDate>" + str(item['stateId']) + ", " + str(dateTime) + "</n:stateName_and_updateDate>"
            xml += "</n:v>"
        xml += "</n:GetListResponse>"
        xml += "</s:Body>"
        xml += "</s:Envelope>"
        

        self.send_response(200)
        self.send_header("Content-type", "application/xml")
        self.end_headers()
        self.wfile.write(xml.encode())

    except Exception as e:
        return generateErrorXml(self, "Cистемная ошибка в коде реализации сервиса /api/hobo-bff/v0.5/MMMS_Request.GetList: " + str(e), False, 0)


def getRequestGet(self, id):
    try:
        url = 'http://10.8.4.244:8010/api/material-movement/v1.0/material-movement-request/' + id
        try:
            r = requests.get(url, headers=headers, timeout=globalTimeout)
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout):
            return generateErrorXml(self, "Сервер СУДМ 10.8.4.244:8010 не ответил на вызов GET /api/material-movement/v1.0/material-movement-request в течение " + str(globalTimeout) + " секунд",  False, 0)
        except Exception as e:
            return generateErrorXml(self, "Ошибка при вызове GET /api/material-movement/v1.0/material-movement-request (Сервер СУДМ 10.8.4.244:8010): " + str(e), False, 0)

        json = r.json()

        xml = "<s:Envelope xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\">"
        xml += "xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\""
        xml += "xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">"
        xml += "<s:Body>"
        xml += "<n:GetResponse xmlns:n=\"urn:MMMS_Request\">"
        xml += "xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\""
        xml += "xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">"
        for item in json['materialMovementRequests']:
            xml += "<n:id>" + str(item['id']) + "</n:id>"
            xml += "<n:stateId>" + str(item['stateId']) + "</n:stateId>"
            xml += "<n:stateName>" + str(item['stateId']) + "</n:stateName>"
            xml += "<n:senderStockId>" + str(item['senderStockId']) + "</n:senderStockId>"
            xml += "<n:senderStockName>" + str(item['senderStockId']) + "</n:senderStockName>"
            xml += "<n:receiverStockId>" + str(item['receiverStockId']) + "</n:receiverStockId>"
            xml += "<n:createDate>" + str(item['createDate']) + "</n:createDate>"
            xml += "<n:stateUpdateDate>" + str(item['createDate']) + "</n:stateUpdateDate>"
            xml += "<n:rejectReasonId>" + str(item['rejectReasonId']) + "</n:rejectReasonId>"
            xml += "<n:rejectReasonName>" + str(item['rejectReasonId']) + "</n:rejectReasonName>"
            xml += "<n:note>" + ifnull(item['note']) + "</n:note>"
            for material in item['materials']:
                xml += "<n:materials>"
                xml += "<material_id>" + str(material['materialId']) + "</material_id>"
                xml += "<material_name>" + ifnull(material['materialName']) + "</material_name>"
                xml += "<unit_name>" +  ifnull(material['materialExternalUnitCode']) + "</unit_name>"
                xml += "<volume>" + str(material['volume']) + "</volume>"
                xml += "</n:materials>"
        xml += "</n:GetResponse>"
        xml += "</s:Body>"
        xml += "</s:Envelope>"
        
        self.send_response(200)
        self.send_header("Content-type", "application/xml")
        self.end_headers()
        self.wfile.write(xml.encode())

    except Exception as e:
        return generateErrorXml(self, "Cистемная ошибка в коде реализации сервиса /api/hobo-bff/v0.5/MMMS_Request.Get: " + str(e), False, 0)


def generateErrorXml(self, err, isCustom, code):
    xml = " <s:Envelope"
    xml += "xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\">"
    xml += "<s:Body>"
    xml += "<s:Fault>"
    xml += "<faultcode>s:Server.userException</faultcode>"
    if(isCustom == True):
        xml += "<faultstring>" + err + str(code) + "</faultstring>"
    else:
        xml += "<faultstring>" + err + "</faultstring>"
    xml += "</s:Fault>"
    xml += "</s:Body>"
    xml += "</s:Envelope>"

    self.send_response(500)
    self.send_header("Content-type", "application/xml")
    self.end_headers()
    self.wfile.write(xml.encode())


run(handler_class=HttpGetHandler)