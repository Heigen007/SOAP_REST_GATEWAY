export default function(arr, type) {
    if(type == "get") {
        
        var xml = `
        <s:Envelope

        xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"
      
        xmlns:xsd="http://www.w3.org/2001/XMLSchema"
      
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
      
          <s:Body>
      
            <n:GetResponse
      
              xmlns:n="urn:MMMS_Request"
      
              xmlns:xsd="http://www.w3.org/2001/XMLSchema"
      
              xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">`

    for (var i = 0; i < arr.length; i++) {
        xml += `
        <n:v>
            <n:id>${arr[i].id}</n:id>

            <n:stateId>${arr[i].stateId}</n:stateId>

            <n:stateName>${arr[i].stateName}</n:stateName>

            <n:senderStockId>${arr[i].senderStockId}</n:senderStockId>

            <n:senderStockName>${arr[i].senderStockName}</n:senderStockName>

            <n:receiverStockId>${arr[i].receiverStockId}</n:receiverStockId>

            <n:createDate>${arr[i].createDate}</n:createDate>

            <n:stateUpdateDate>${arr[i].stateUpdateDate}</n:stateUpdateDate>

            <n:rejectReasonId>${arr[i].rejectReasonId}</n:rejectReasonId>

            <n:rejectReasonName>${arr[i].rejectReasonName}</n:rejectReasonName>

            <n:note>${arr[i].note}</n:note>` + buildMaterialInfo(arr[i].materials) +  `
        </n:v>`
    }

    xml+=`

    </n:GetResponse>

    </s:Body>

</s:Envelope>`
    } else if(type == "list") {
        var xml = `
        <s:Envelope

        xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"
      
        xmlns:xsd="http://www.w3.org/2001/XMLSchema"
      
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
      
          <s:Body>
      
            <n:GetResponse
      
              xmlns:n="urn:MMMS_Request"
      
              xmlns:xsd="http://www.w3.org/2001/XMLSchema"
      
              xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">`

    for (var i = 0; i < arr.length; i++) {
        xml += `
        <n:v>
            <n:id>${arr[i].id}</n:id>

            <n:stateName>${arr[i].stateName || arr[i].stateId}</n:stateName>

            <n:senderStockName>${arr[i].senderStockName || arr[i].senderStockId}</n:senderStockName>

            <n:stateUpdateDate>${arr[i].stateUpdateDate || arr[i].createDate}</n:stateUpdateDate>

            <n:stateName_and_UpdateDate>${arr[i].stateName || arr[i].stateId}, ${timeToAlmatyTimezone(arr[i].stateUpdateDate || arr[i].createDate)}</n:stateName_and_UpdateDate>
        </n:v>`
    }


    xml+=`

    </n:GetResponse>

    </s:Body>

</s:Envelope>`
    }
    return xml

}

function buildMaterialInfo(arr) {
    var tempXml = ""
    for(var i = 0; i < arr.length; i++) {

        tempXml += `
        <n:materials>
            <material_id>${arr[i].materialId}</material_id>
            <material_name>${arr[i].materialName}</material_name>
            <unit_name>${arr[i].materialExternalUnitCode}</unit_name>
            <volume>${arr[i].volume}</volume>
        </n:materials>
        `
    }
    return tempXml
}

function timeToAlmatyTimezone(time) {
    

    var date = new Date(time);
    date.setHours(date.getHours() + (date.getTimezoneOffset() / 60));
    date.setHours(date.getHours() + 6);
    var temp = ""
    // date to format: "yyyy-mm-dd hh:mm:ss"
    temp += String(date.getDate()).length == 2 ? date.getDate() + "." : "0" + date.getDate() + "."
    temp += (String(date.getMonth() + 1)).length == 2 ? (date.getMonth() + 1) + "." : "0" + (date.getMonth() + 1) + "."
    temp += date.getFullYear() + " "
    temp += String(date.getHours()).length == 2 ? date.getHours() + ":" : "0" + date.getHours() + ":"
    temp += String(date.getMinutes()).length == 2 ? date.getMinutes() + ":" : "0" + date.getMinutes() + ":"
    temp += String(date.getSeconds()).length == 2 ? date.getSeconds() : "0" + date.getSeconds()

    return temp
}