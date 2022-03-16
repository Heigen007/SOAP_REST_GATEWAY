import requests # You should install "requests" on the host machine
from generateErrorXml import generateErrorXml
from ifnull import ifnull

headers = {'AUTHORIZATION':'123'}
globalTimeout = 20

def getStockList(self):
    try:
        url = 'http://10.8.4.244:8010/api/material-movement-be/v1.0/stock'
        try:
            r = requests.get(url, headers=headers, timeout=globalTimeout)
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout):
            return generateErrorXml(self, "Сервер СУДМ 10.8.4.244:8010 не ответил на вызов GET /api/material-movement-be/v1.0/stock в течение " + str(globalTimeout) + " секунд",  False, 0)
        except Exception as e:
            return generateErrorXml(self, "Ошибка при вызове GET /api/material-movement-be/v1.0/stock (Сервер СУДМ 10.8.4.244:8010): " + str(e), False, 0)

        json = r.json()

        if('stocks' not in json):
            return generateErrorXml(self, "От сервера СУДМ 10.8.4.244:8010 на вызов GET /api/material-movement-be/v1.0/stock получен неожиданный ответ:", True, r.status_code)
        elif(json['stocks'] == []):
            return generateErrorXml(self, "От сервера СУДМ 10.8.4.244:8010 на вызов GET-метода /api/material-movement-be/v1.0/stock получен пустой список складов", False, 0)

        xml = "<s:Envelope "
        xml += "xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\" "
        xml += "xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" "
        xml += "xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">"
        xml += "<s:Body>"
        xml += "<n:GetListResponse "
        xml += "xmlns:n=\"urn:MMMS_Stock\" "
        xml += "xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" "
        xml += "xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">"
        for item in json['stocks']:
            xml += "<n:v>"
            xml += "<n:id>" + ifnull(item.get('id')) + "</n:id>"
            xml += "<n:name>" + ifnull(item.get('name')) + "</n:name>"
            xml += "</n:v>"
        xml += "</n:GetListResponse>"
        xml += "</s:Body>"
        xml += "</s:Envelope>"

        self.send_response(200)
        self.send_header("Content-type", "application/xml")
        self.end_headers()
        self.wfile.write(xml.encode())
    except Exception as e:
        return generateErrorXml(self, "Cистемная ошибка в коде реализации метода /api/hobo-bff/v0.5/MMMS_Stock.GetList: " + str(e), False, 0)