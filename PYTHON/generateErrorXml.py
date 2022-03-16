def generateErrorXml(self, err, isCustom, code):
    xml =  "<s:Envelope xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\">"
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