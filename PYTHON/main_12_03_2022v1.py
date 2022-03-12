from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import xml.etree.ElementTree as ET
import requests
# import datetime


headers = {'AUTHORIZATION': '123'}
globalTimeout = 20


def ifnull(var):
    if var is None: return ""
    if isinstance(var, int): return str(var)
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
        elif self.path == "/api/hobo-bff/v0.5/MMMS_Material_In_Stock":
            getMaterialInStock(self)


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
            return generateErrorXml(self, "От сервера СУДМ 10.8.4.244:8010 на вызов GET-метода /api/material-movement/v1.0/stock получен пустой список складов", False, 0)

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
            xml += "<ns0:id>" + ifnull(item.get('id')) + "</ns0:id>"
            xml += "<ns0:name>" + ifnull(item.get('name')) + "</ns0:name>"
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
            return generateErrorXml(self, "Сервер СУДМ 10.8.4.244:8010 не ответил на вызов GET /api/material-movement/v1.0/material-movement-request?stockId=" + id + '&dateFrom=2022-01-01T00:00:00+06:00 в течение ' + str(globalTimeout) + " секунд",  False, 0)
        except Exception as e:
            return generateErrorXml(self, "Ошибка при вызове GET /api/material-movement/v1.0/material-movement-request?stockId=" + id + "&dateFrom=2022-01-01T00:00:00+06:00 (Сервер СУДМ 10.8.4.244:8010): " + str(e), False, 0)
        
        json = r.json()

        if(json is None or 'materialMovementRequests' not in json):
            return generateErrorXml(self, "От сервера СУДМ 10.8.4.244:8010 на вызов GET /api/material-movement/v1.0/material-movement-request?stockId=" + id + '&dateFrom=2022-01-01T00:00:00+06:00  получен неожиданный ответ: ', True, r.status_code)
        elif(json['materialMovementRequests'] == []):
            return generateErrorXml(self, "От сервера СУДМ 10.8.4.244:8010 на вызов GET-метода /api/material-movement/v1.0/material-movement-request?stockId=" + id + "&dateFrom=2022-01-01T00:00:00+06:00 получен пустой список materialMovementRequests",False, 0)

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
            t = item.get('createDate')
            if(t is not None): dateTime = " ".join(t.split('T'))
            else: dateTime = ""
            #dateTime = datetime.datetime(int(t.split('-')[0]), int(t.split('-')[1]), int(t.split('T')[0].split('-')[2]), int(t.split('T')[1].split(':')[0]), int(t.split(':')[1]), int(t.split(':')[2]))
            #hours_added = datetime.timedelta(hours = int(t.split("+")[1].split(":")[0]) - 6, minutes = int(t.split("+")[1].split(":")[1]))
            #dateTime -= hours_added
            xml += "<n:v>"
            xml += "<n:id>" + ifnull(item.get('id')) + "</n:id>"
            xml += "<n:stateName>" + ifnull(item.get('stateName')) + "</n:stateName>"
            xml += "<n:senderStockName>" + ifnull(item.get('senderStockName')) + "</n:senderStockName>"
            xml += "<n:stateUpdateDate>" + ifnull(item.get('createDate')) + "</n:stateUpdateDate>"
            xml += "<n:stateName_and_updateDate>" + ifnull(item.get('stateName')) + ", " + str(dateTime) + "</n:stateName_and_updateDate>"
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
            return generateErrorXml(self, "Сервер СУДМ 10.8.4.244:8010 не ответил на вызов GET /api/material-movement/v1.0/material-movement-request/" + id + " в течение " + str(globalTimeout) + " секунд",  False, 0)
        except Exception as e:
            return generateErrorXml(self, "Ошибка при вызове GET /api/material-movement/v1.0/material-movement-request/" + id + " (Сервер СУДМ 10.8.4.244:8010): " + str(e), False, 0)

        json = r.json()

        if(json is None or 'materialMovementRequests' not in json):
            return generateErrorXml(self, "От сервера СУДМ 10.8.4.244:8010 на вызов GET /api/material-movement/v1.0/material-movement-request/" + id + " получен неожиданный ответ:", True, r.status_code)
        elif(json['materialMovementRequests'] == []):
            return generateErrorXml(self, "От сервера СУДМ 10.8.4.244:8010 на вызов GET-метода /api/material-movement/v1.0/material-movement-request/" + id + " получен пустой список materialMovementRequests",False, 0)

        xml = "<s:Envelope xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\">"
        xml += "xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\""
        xml += "xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">"
        xml += "<s:Body>"
        xml += "<n:GetResponse xmlns:n=\"urn:MMMS_Request\">"
        xml += "xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\""
        xml += "xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">"
        for item in json['materialMovementRequests']:
            xml += "<n:id>" + ifnull(item.get('id')) + "</n:id>"
            xml += "<n:stateId>" + ifnull(item.get('stateId')) + "</n:stateId>"
            xml += "<n:stateName>" + ifnull(item.get('stateName')) + "</n:stateName>"
            xml += "<n:senderStockId>" + ifnull(item.get('senderStockId')) + "</n:senderStockId>"
            xml += "<n:senderStockName>" + ifnull(item.get('senderStockName')) + "</n:senderStockName>"
            xml += "<n:receiverStockId>" + ifnull(item.get('receiverStockId')) + "</n:receiverStockId>"
            xml += "<n:createDate>" + ifnull(item.get('createDate')) + "</n:createDate>"
            xml += "<n:stateUpdateDate>" + ifnull(item.get('stateUpdateDate')) + "</n:stateUpdateDate>"
            xml += "<n:rejectReasonId>" + ifnull(item.get('rejectReasonId')) + "</n:rejectReasonId>"
            xml += "<n:rejectReasonName>" + ifnull(item.get('rejectReasonName')) + "</n:rejectReasonName>"
            xml += "<n:note>" + ifnull(item.get('note')) + "</n:note>"
            for material in item['materials']:
                xml += "<n:materials>"
                xml += "<id>" + ifnull(material.get('materialId')) + "</id>"
                xml += "<material>" + ifnull(material.get('materialName')) + "</material>"
                xml += "<unit>" + ifnull(material.get('materialExternalUnitCode')) + "</unit>"
                xml += "<volume>" + ifnull(material.get('volume')) + "</volume>"
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

def getMaterialInStock(self):
    try:
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)
        myroot = ET.fromstring(post_body)
        id = myroot[0][0][0].text

        url = 'http://10.8.4.244:8010/api/material-movement/v1.0/stock/' + id + '/material-in-stock'
        try:
            r = requests.get(url, headers=headers, timeout=globalTimeout)
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout):
            return generateErrorXml(self, "Сервер СУДМ 10.8.4.244:8010 не ответил на вызов GET /api/material-movement/v1.0/stock/" + id + "/material-in-stock в течение " + str(globalTimeout) + " секунд",  False, 0)
        except Exception as e:
            return generateErrorXml(self, "Ошибка при вызове GET /api/material-movement/v1.0/stock/" + id + "/material-in-stock (Сервер СУДМ 10.8.4.244:8010): " + str(e), False, 0)
        
        json = r.json()

        if(json is None or 'materialsInStock' not in json):
            return generateErrorXml(self, "От сервера СУДМ 10.8.4.244:8010 на вызов GET /api/material-movement/v1.0/stock/" + id + "/material-in-stock получен неожиданный ответ:", True, r.status_code)
        elif(json['materialsInStock'] == []):
            return generateErrorXml(self, "От сервера СУДМ 10.8.4.244:8010 на вызов GET-метода /api/material-movement/v1.0/stock/" + id + "/material-in-stock получен пустой список materialsInStock",False, 0)

        xml= "<soapenv:Envelope"
        xml+= "xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\""
        xml+= "xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\""
        xml+= "xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">"
        xml+= "<soapenv:Body>"
        xml+= "<n:GetListResponse"
        xml+= "xmlns:n=\"urn:MMMS_Material_In_Stock\""
        xml+= "xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\""
        xml+= "xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">"
        for item in json['materialsInStock']:
            xml += "<n:v>"
            xml += "<n:id>" + ifnull(item.get('id')) + "</n:id>"
            xml += "<n:material_id>" + ifnull(item.get('materialId')) + "</n:material_id>"
            xml += "<n:material_name>" + ifnull(item.get('materialName')) + "</n:material_name>"
            xml += "<n:unit>" + ifnull(item.get('materialExternalUnitCode')) + "</n:unit>"
            xml += "</n:v>"
        xml += "</n:GetListResponse>"
        xml += "</soapenv:Body>"
        xml += "</soapenv:Envelope>"
        

        self.send_response(200)
        self.send_header("Content-type", "application/xml")
        self.end_headers()
        self.wfile.write(xml.encode())

    except Exception as e:
        return generateErrorXml(self, "Cистемная ошибка в коде реализации сервиса /api/hobo-bff/v0.5/MMMS_Material_In_Stock: " + str(e), False, 0)


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