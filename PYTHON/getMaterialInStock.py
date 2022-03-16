from generateErrorXml import generateErrorXml
import xml.etree.ElementTree as ET
from getMaterialInStockGetList import getMaterialInStockGetList
from getMaterialInStockGetMaterialTypeList import getMaterialInStockGetMaterialTypeList
from getMaterialInStockGetMaterialList import getMaterialInStockGetMaterialList

headers = {'AUTHORIZATION':'123'}
globalTimeout = 20

def getMaterialInStock(self):
    try:
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)
        myroot = ET.fromstring(post_body)
        for child in myroot:
            if child.tag.split("}")[1] == "Body": 
                myroot = child
                break
        id = ''
        typeId = ''

        if(myroot[0].tag.split('}')[1] == "GetList"):
            for child in myroot[0]:
                if child.tag == 'Stock_ID': id = child.text
            if id == '': return generateErrorXml(self, "Cистемная ошибка в коде реализации метода сервиса /api/hobo-bff/v0.5/MMMS_Material_In_Stock.GetList: Stock_ID является обязательным параметром", False, 0)
            if not id.isdigit(): return generateErrorXml(self, "Cистемная ошибка в коде реализации метода сервиса /api/hobo-bff/v0.5/MMMS_Material_In_Stock.GetList: Stock_ID должен быть целым числом", False, 0)
            getMaterialInStockGetList(self, id)
        elif(myroot[0].tag.split('}')[1] == "GetMaterialTypeList"):
            for child in myroot[0]:
                if child.tag == "stock_id": id = child.text
            if id == '': return generateErrorXml(self, "Cистемная ошибка в коде реализации метода сервиса /api/hobo-bff/v0.5/MMMS_Material_In_Stock.GetMaterialTypeList: stock_id является обязательным параметром", False, 0)
            if not id.isdigit(): return generateErrorXml(self, "Cистемная ошибка в коде реализации метода сервиса /api/hobo-bff/v0.5/MMMS_Material_In_Stock.GetMaterialTypeList: stock_id должен быть целым числом", False, 0)
            getMaterialInStockGetMaterialTypeList(self, id)
        elif(myroot[0].tag.split('}')[1] == "GetMaterialList"):
            for child in myroot[0]:
                if child.tag == "stock_id": id = child.text
                if child.tag == "type_id": typeId = child.text
            if id == '': return generateErrorXml(self, "Cистемная ошибка в коде реализации метода сервиса /api/hobo-bff/v0.5/MMMS_Material_In_Stock.GetMaterialList: stock_id является обязательным параметром", False, 0)
            if typeId == '': return generateErrorXml(self, "Cистемная ошибка в коде реализации метода сервиса /api/hobo-bff/v0.5/MMMS_Material_In_Stock.GetMaterialList: type_id является обязательным параметром", False, 0)
            if not id.isdigit(): return generateErrorXml(self, "Cистемная ошибка в коде реализации метода сервиса /api/hobo-bff/v0.5/MMMS_Material_In_Stock.GetMaterialList: stock_id должен быть целым числом", False, 0)
            if not typeId.isdigit(): return generateErrorXml(self, "Cистемная ошибка в коде реализации метода сервиса /api/hobo-bff/v0.5/MMMS_Material_In_Stock.GetMaterialList: type_id должен быть целым числом", False, 0)
            getMaterialInStockGetMaterialList(self, id, int(typeId))
    except Exception as e:
        return generateErrorXml(self, "Cистемная ошибка в коде реализации сервиса /api/hobo-bff/v0.5/MMMS_Material_In_Stock: " + str(e), False, 0)