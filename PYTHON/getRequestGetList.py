import requests # You should install "requests" on the host machine
from generateErrorXml import generateErrorXml
from ifnull import ifnull

headers = {'AUTHORIZATION':'123'}
globalTimeout = 20

def getRequestGetList(self, id):
    try:
        url = 'http://10.8.4.244:8010/api/material-movement-be/v1.0/material-movement-request?receiverStockId=' + id
        try:
            r = requests.get(url, headers=headers, timeout=globalTimeout)
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout):
            return generateErrorXml(self, "Сервер СУДМ 10.8.4.244:8010 не ответил на вызов GET /api/material-movement-be/v1.0/material-movement-request?receiverStockId=" + id + ' в течение ' + str(globalTimeout) + " секунд",  False, 0)
        except Exception as e:
            return generateErrorXml(self, "Ошибка при вызове GET /api/material-movement-be/v1.0/material-movement-request?receiverStockId=" + id + " (сервер СУДМ 10.8.4.244:8010): " + str(e), False, 0)
        
        json = r.json()

        if(json is None or 'materialMovementRequests' not in json):
            return generateErrorXml(self, "От сервера СУДМ 10.8.4.244:8010 на вызов GET /api/material-movement-be/v1.0/material-movement-request?receiverStockId=" + id + ' получен неожиданный ответ: ', True, r.status_code)
        elif(json['materialMovementRequests'] == []):
            return generateErrorXml(self, "От сервера СУДМ получен пустой список заявок", False, 0)

        xml= "<s:Envelope "
        xml+= "xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\" "
        xml+= "xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" "
        xml+= "xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">"
        xml+= "<s:Body>"
        xml+= "<n:GetListResponse "
        xml+= "xmlns:n=\"urn:MMMS_Request\" "
        xml+= "xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" "
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
            # xml += "<n:senderStockName>" + "Склад отправителя: " + ifnull(item.get('senderStockName')) + "</n:senderStockName>"
            xml += "<n:createDate>Дата создания: " + ifnull(item.get('createDate')) + "</n:createDate>"
            xml += "<n:stateInfo>Статус: " + ifnull(item.get('stateName')) + ", дата изменения: " + str(dateTime) + "</n:stateInfo>"
            xml += "</n:v>"
        xml += "</n:GetListResponse>"
        xml += "</s:Body>"
        xml += "</s:Envelope>"

        self.send_response(200)
        self.send_header("Content-type", "application/xml")
        self.end_headers()
        self.wfile.write(xml.encode())

    except Exception as e:
        return generateErrorXml(self, "Cистемная ошибка в коде реализации метода /api/hobo-bff/v0.5/MMMS_Request.GetList: " + str(e), False, 0)