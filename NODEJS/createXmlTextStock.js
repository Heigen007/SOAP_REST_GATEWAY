export default function(arr) {
    var xml = `
    <soapenv:Envelope

xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"

xmlns:xsd="http://www.w3.org/2001/XMLSchema"

xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

<soapenv:Body>

  <ns0:GetListResponse

    xmlns:ns0="urn:Get_MMMS_Stock_List"

    xmlns:xsd="http://www.w3.org/2001/XMLSchema"

    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">`

    for (var i = 0; i < arr.length; i++) {
        xml += `
        <ns0:v>
            <ns0:id>${arr[i].id}</ns0:id>
            <ns0:name>${arr[i].name}</ns0:name>
        </ns0:v>`
    }

    xml+=`

  </ns0:GetListResponse>

</soapenv:Body>

</soapenv:Envelope>`

return xml;

}