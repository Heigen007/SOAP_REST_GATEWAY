import requests # You should install "requests" on the host machine
from generateErrorXml import generateErrorXml
from ifnull import ifnull

headers = {'AUTHORIZATION':'123'}
globalTimeout = 20

def getMaterialInStockGetMaterialTypeList(self, id):
    try:
        url = 'http://10.8.4.244:8010/api/material-movement-be/v1.0/stock/' + id + '/material-in-stock'
        try:
            r = requests.get(url, headers=headers, timeout=globalTimeout)
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout):
            return generateErrorXml(self, "Сервер СУДМ 10.8.4.244:8010 не ответил на вызов GET /api/material-movement-be/v1.0/stock/" + id + "/material-in-stock в течение " + str(globalTimeout) + " секунд",  False, 0)
        except Exception as e:
            return generateErrorXml(self, "Ошибка при вызове GET /api/material-movement-be/v1.0/stock/" + id + "/material-in-stock (Сервер СУДМ 10.8.4.244:8010): " + str(e), False, 0)
        
        json = r.json()

        if(json is None or 'materialsInStock' not in json):
            return generateErrorXml(self, "От сервера СУДМ 10.8.4.244:8010 на вызов GET /api/material-movement-be/v1.0/stock/" + id + "/material-in-stock получен неожиданный ответ:", True, r.status_code)
        elif(json['materialsInStock'] == []):
            return generateErrorXml(self, "Для выбранного склада СУДМ получен пустой список расходных материалов", False, 0)

        xml= "<s:Envelope "
        xml+= "xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\" "
        xml+= "xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" "
        xml+= "xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">"
        xml+= "<s:Body>"
        xml+= "<n:GetMaterialTypeListResponse "
        xml+= "xmlns:n=\"urn:MMMS_Material_In_Stock\" "
        xml+= "xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" "
        xml+= "xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">"

        uniqueType = set()
        for item in json['materialsInStock']: uniqueType.add((ifnull(item.get('materialTypeId')),ifnull(item.get('materialTypeName'))))
        for item in uniqueType:
            xml += "<n:v>"
            xml += "<n:type_id>" + item[0] + "</n:type_id>"
            xml += "<n:type_name>" + item[1] + "</n:type_name>"
            xml += "</n:v>"

        xml += "</n:GetMaterialTypeListResponse>"
        xml += "</s:Body>"
        xml += "</s:Envelope>"

        self.send_response(200)
        self.send_header("Content-type", "application/xml")
        self.end_headers()
        self.wfile.write(xml.encode())

    except Exception as e:
        return generateErrorXml(self, "Cистемная ошибка в коде реализации сервиса /api/hobo-bff/v0.5/MMMS_Material_In_Stock.GetMaterialTypeList: " + str(e), False, 0)