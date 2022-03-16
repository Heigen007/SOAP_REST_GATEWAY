from generateErrorXml import generateErrorXml
from getRequestGetList import getRequestGetList
from getRequestGet import getRequestGet
from getRequestGetMaterialList import getRequestGetMaterialList

import xml.etree.ElementTree as ET

def getRequest(self):
    try:
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)
        myroot = ET.fromstring(post_body)
        for child in myroot:
            if child.tag.split("}")[1] == "Body": 
                myroot = child
                break
        id = ''

        if(myroot[0].tag.split('}')[1] == "GetList"):
            for child in myroot[0]:
                if child.tag == 'Stock_ID_Receiver': id = child.text
            if id == '': return generateErrorXml(self, "Cистемная ошибка в коде реализации метода сервиса /api/hobo-bff/v0.5/MMMS_Request.GetList: Stock_ID_Receiver является обязательным параметром", False, 0)
            if not id.isdigit(): return generateErrorXml(self, "Cистемная ошибка в коде реализации метода сервиса /api/hobo-bff/v0.5/MMMS_Request.GetList: Stock_ID_Receiver должен быть целым числом", False, 0)
            getRequestGetList(self, id)
        elif(myroot[0].tag.split('}')[1] == 'Get'):
            for child in myroot[0]:
                if child.tag == "Request_ID": id = child.text
            if id == '': return generateErrorXml(self, "Cистемная ошибка в коде реализации метода сервиса /api/hobo-bff/v0.5/MMMS_Request.Get: Request_ID является обязательным параметром", False, 0)
            if not id.isdigit(): return generateErrorXml(self, "Cистемная ошибка в коде реализации метода сервиса /api/hobo-bff/v0.5/MMMS_Request.Get: Request_ID должен быть целым числом", False, 0)
            getRequestGet(self, id)
        elif(myroot[0].tag.split('}')[1] == "GetMaterialList"):
            for child in myroot[0]:
                if child.tag == "request_id": id = child.text
            if id == '': return generateErrorXml(self, "Cистемная ошибка в коде реализации метода сервиса /api/hobo-bff/v0.5/MMMS_Request.GetMaterialList: request_id является обязательным параметром", False, 0)
            if not id.isdigit(): return generateErrorXml(self, "Cистемная ошибка в коде реализации метода сервиса /api/hobo-bff/v0.5/MMMS_Request.GetMaterialList: request_id должен быть целым числом", False, 0)
            getRequestGetMaterialList(self, id)
    except Exception as e:
        return generateErrorXml(self, "Cистемная ошибка в коде реализации сервиса /api/hobo-bff/v0.5/MMMS_Request: " + str(e), False, 0)