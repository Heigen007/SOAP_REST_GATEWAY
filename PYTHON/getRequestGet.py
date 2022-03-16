import requests # You should install "requests" on the host machine
from generateErrorXml import generateErrorXml
from ifnull import ifnull

headers = {'AUTHORIZATION':'123'}
globalTimeout = 20

# Получение данных о заявке на перемещение
def getRequestGet(self, id):
    try:
        url = 'http://10.8.4.244:8010/api/material-movement-be/v1.0/material-movement-request/' + id
        try:
            r = requests.get(url, headers=headers, timeout=globalTimeout)
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout):
            return generateErrorXml(self, "Сервер СУДМ 10.8.4.244:8010 не ответил на вызов GET /api/material-movement-be/v1.0/material-movement-request/" + id + " в течение " + str(globalTimeout) + " секунд",  False, 0)
        except Exception as e:
            return generateErrorXml(self, "Ошибка при вызове GET /api/material-movement-be/v1.0/material-movement-request/" + id + " (сервер СУДМ 10.8.4.244:8010): " + str(e), False, 0)

        json = r.json()

        if(json is None or 'materialMovementRequests' not in json):
            return generateErrorXml(self, "От сервера СУДМ 10.8.4.244:8010 на вызов GET /api/material-movement-be/v1.0/material-movement-request/" + id + " получен неожиданный ответ:", True, r.status_code)
        elif(json['materialMovementRequests'] == []):
            return generateErrorXml(self, "От сервера СУДМ 10.8.4.244:8010 на вызов GET /api/material-movement-be/v1.0/material-movement-request/" + id + " получен пустой ответ", False, 0)

        xml = "<s:Envelope xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\" "
        xml += "xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" "
        xml += "xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">"
        xml += "<s:Body>"
        xml += "<n:GetResponse xmlns:n=\"urn:MMMS_Request\" "
        xml += "xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" "
        xml += "xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">"
        for item in json['materialMovementRequests']:
            xml += "<n:id>" + ifnull(item.get('id')) + "</n:id>"
            #xml += "<n:stateId>" + ifnull(item.get('stateId')) + "</n:stateId>"
            xml += "<n:stateName>" + ifnull(item.get('stateName')) + "</n:stateName>"
            xml += "<n:senderStockId>" + ifnull(item.get('senderStockId')) + "</n:senderStockId>"
            xml += "<n:senderStockName>" + ifnull(item.get('senderStockName')) + "</n:senderStockName>"
            xml += "<n:receiverStockId>" + ifnull(item.get('receiverStockId')) + "</n:receiverStockId>"
            xml += "<n:createDate>" + ifnull(item.get('createDate')) + "</n:createDate>"
            xml += "<n:stateUpdateDate>" + ifnull(item.get('stateUpdateDate')) + "</n:stateUpdateDate>"
            xml += "<n:rejectReasonId>" + ifnull(item.get('rejectReasonId')) + "</n:rejectReasonId>"
            xml += "<n:rejectReasonName>" + ifnull(item.get('rejectReasonName')) + "</n:rejectReasonName>"
            xml += "<n:note>" + ifnull(item.get('note')) + "</n:note>"
            #if item.get('materialMovementRequestItems'):
            #    for material in item.get('materialMovementRequestItems'):
            #        xml += "<n:material>"
            #        xml += "<id>" + ifnull(material.get('materialId')) + "</id>"
            #        xml += "<name>" + ifnull(material.get('materialName')) + "</name>"
            #        xml += "<unit>" + ifnull(material.get('materialExternalUnitCode')) + "</unit>"
            #        xml += "<volume>" + ifnull(material.get('volume')) + "</volume>"
            #        xml += "</n:material>"
        xml += "</n:GetResponse>"
        xml += "</s:Body>"
        xml += "</s:Envelope>"
        
        self.send_response(200)
        self.send_header("Content-type", "application/xml")
        self.end_headers()
        self.wfile.write(xml.encode())

    except Exception as e:
        return generateErrorXml(self, "Cистемная ошибка в коде реализации метода /api/hobo-bff/v0.5/MMMS_Request.Get: " + str(e), False, 0)