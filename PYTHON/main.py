from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import xml.etree.ElementTree as ET
import requests
import datetime

headers = {'AUTHORIZATION': '123'}
globalTimeout = 20

def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
  server_address = ('', 8000)
  httpd = server_class(server_address, handler_class)
  try:
      httpd.serve_forever()
  except KeyboardInterrupt:
      httpd.server_close()

class HttpGetHandler(BaseHTTPRequestHandler):
    """Обработчик с реализованным методом do_GET."""

    def do_POST(self):
        if self.path == "/api/hobo-bff/v0.5/MMMS_Stock":
            getStockList(self)
        elif self.path == "/api/hobo-bff/v0.5/MMMS_Request":
            getRequest(self)

##############################################################################3

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

        xml = " <soapenv:Envelope\n"
        xml += "   xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\"\n"
        xml += "   xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\"\n"
        xml += "   xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">\n"
        xml += "   <soapenv:Body>\n"
        xml += "     <ns0:GetListResponse\n"
        xml += "       xmlns:ns0=\"urn:MMMS_Hobo_Movement_Request_Join\"\n"
        xml += "       xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\"\n"
        xml += "       xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">\n"
        for item in json['stocks']:
            xml += "       <ns0:v>\n"
            xml += "         <ns0:id>" + str(item['id']) + "</ns0:id>\n"
            xml += "         <ns0:name>" + item['name'] + "</ns0:name>\n"
            xml += "       </ns0:v>\n"
        xml += "     </ns0:GetListResponse>\n"
        xml += "   </soapenv:Body>\n"
        xml += " </soapenv:Envelope>\n"


        self.send_response(200)
        self.send_header("Content-type", "application/xml")
        self.end_headers()
        self.wfile.write(xml.encode())
    except Exception as e:
        return generateErrorXml(self, "Cистемная ошибка в коде реализации сервиса /api/hobo-bff/v0.5/MMMS_Stock.GetList: " + str(e), False, 0)

#########################################################################################33

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

####################################################################################################

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
        xml= " <s:Envelope\n"
        xml+= "   xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\"\n"
        xml+= "   xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\"\n"
        xml+= "   xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">\n"
        xml+= "   <s:Body>\n"
        xml+= "     <n:GetListResponse\n"
        xml+= "       xmlns:n=\"urn:MMMS_Request\"\n"
        xml+= "       xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\"\n"
        xml+= "       xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">\n"
        for item in json['materialMovementRequests']:
            # 2012-04-23T18:25:43.511000+00:00
            t = item['createDate']
            hours_added = datetime.timedelta(hours = int(t.split("+")[1].split(":")[0]) - 6, minutes = int(t.split("+")[1].split(":")[1]))
            dateTime = datetime.datetime(int(t.split('-')[0]), int(t.split('-')[1]), int(t.split('T')[0].split('-')[2]), int(t.split('T')[1].split(':')[0]), int(t.split(':')[1]), int(t.split(':')[2].split('.')[0]))
            dateTime -= hours_added
            xml += "       <n:v>\n"
            xml += "         <n:id>" + str(item['id']) + "</n:id>\n"
            xml += "         <n:stateName>" + str(item['stateId']) + "</n:stateName>\n"
            xml += "         <n:senderStockName>" + str(item['senderStockId']) + "</n:senderStockName>\n"
            xml += "         <n:stateUpdateDate>" + item['createDate'] + "</n:stateUpdateDate>\n"
            xml += "         <n:stateName_and_updateDate>" + str(item['stateId']) + ", " + str(dateTime) + "</n:stateName_and_updateDate>\n"
            xml += "       </n:v>\n"
        xml += "     </n:GetListResponse>\n"
        xml += "   </s:Body>\n"
        xml += " </s:Envelope>\n"
        

        self.send_response(200)
        self.send_header("Content-type", "application/xml")
        self.end_headers()
        self.wfile.write(xml.encode())

    except Exception as e:
        return generateErrorXml(self, "Cистемная ошибка в коде реализации сервиса /api/hobo-bff/v0.5/MMMS_Request.GetList: " + str(e), False, 0)

#######################################################################################################

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

        xml = "<s:Envelope xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\">\n"
        xml += "   xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\"\n"
        xml += "   xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">\n"
        xml += "   <s:Body>\n"
        xml += "     <n:GetResponse xmlns:n=\"urn:MMMS_Request\">\n"
        xml += "       xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\"\n"
        xml += "       xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">\n"
        for item in json['materialMovementRequests']:
            xml += "       <n:v>\n"
            xml += "         <n:id>" + str(item['id']) + "</n:id>\n"
            xml += "         <n:stateId>" + str(item['stateId']) + "</n:stateId>\n"
            xml += "         <n:stateName>" + str(item['stateId']) + "</n:stateName>\n"
            xml += "         <n:senderStockId>" + str(item['senderStockId']) + "</n:senderStockId>\n"
            xml += "         <n:senderStockName>" + str(item['senderStockId']) + "</n:senderStockName>\n"
            xml += "         <n:receiverStockId>" + str(item['receiverStockId']) + "</n:receiverStockId>\n"
            xml += "         <n:createDate>" + str(item['createDate']) + "</n:createDate>\n"
            xml += "         <n:stateUpdateDate>" + str(item['createDate']) + "</n:stateUpdateDate>\n"
            xml += "         <n:rejectReasonId>" + str(item['rejectReasonId']) + "</n:rejectReasonId>\n"
            xml += "         <n:rejectReasonName>" + str(item['rejectReasonId']) + "</n:rejectReasonName>\n"
            xml += "         <n:note>" + str(item['note']) + "</n:note>\n"
            for material in item['materials']:
                xml += "         <n:materials>\n"
                xml += "           <material_id>" + str(material['materialId']) + "</material_id>\n"
                xml += "           <material_name>" + str(material['materialName']) + "</material_name>\n"
                xml += "           <unit_name>" + str(material['materialExternalUnitCode']) + "</unit_name>\n"
                xml += "           <volume>" + str(material['volume']) + "</volume>\n"
                xml += "         </n:materials>\n"
            xml += "       </n:v>\n"
        xml += "     </n:GetResponse>\n"
        xml += "   </s:Body>\n"
        xml += " </s:Envelope>\n"
        

        self.send_response(200)
        self.send_header("Content-type", "application/xml")
        self.end_headers()
        self.wfile.write(xml.encode())

    except Exception as e:
        return generateErrorXml(self, "Cистемная ошибка в коде реализации сервиса /api/hobo-bff/v0.5/MMMS_Request.Get: " + str(e), False, 0)

#######################################################################################################

def generateErrorXml(self, err, isCustom, code):
    xml = " <s:Envelope\n"
    xml += "   xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\">\n"
    xml += "   <s:Body>\n"
    xml += "     <s:Fault>\n"
    xml += "       <faultcode>s:Server.userException</faultcode>\n"
    if(isCustom == True):
        xml += "       <faultstring>" + err + str(code) + "</faultstring>\n"
    else:
        xml += "       <faultstring>" + err + "</faultstring>\n"
    xml += "     </s:Fault>\n"
    xml += "   </s:Body>\n"
    xml += " </s:Envelope>\n"

    self.send_response(500)
    self.send_header("Content-type", "application/xml")
    self.end_headers()
    self.wfile.write(xml.encode())


run(handler_class=HttpGetHandler)