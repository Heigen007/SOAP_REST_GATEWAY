export default function(param, ExtraException, errCode) {
    if(param === "NoStocks") return `
    <s:Envelope

    xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">

  <s:Body>

    <s:Fault>

      <faultcode>s:Server.userException</faultcode>

      <faultstring>От сервера СУДМ 10.8.4.244:8010 на вызов GET /api/material-movement/v1.0/stock получен неожиданный ответ: ` + errCode + `</faultstring>

    </s:Fault>

  </s:Body>

</s:Envelope>
    `
    else if(param === "EmptyStocks") return `
    <s:Envelope

    xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">

  <s:Body>

    <s:Fault>

      <faultcode>s:Server.userException</faultcode>

      <faultstring>От сервера СУДМ 10.8.4.244:8010 на вызов GET-метода /api/material-movement/v1.0/stock получен пустой список складов</faultstring>

    </s:Fault>

  </s:Body>

</s:Envelope>
    `
    else if(param === "NoMaterialMovementRequests") return `
    <s:Envelope

    xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">

  <s:Body>

    <s:Fault>

      <faultcode>s:Server.userException</faultcode>

      <faultstring>От сервера СУДМ 10.8.4.244:8010 на вызов GET /api/material-movement/v1.0/material-movement-request получен неожиданный ответ: ` + errCode + `</faultstring>

    </s:Fault>

  </s:Body>

</s:Envelope>`
    else if(param === "EmptyMaterialMovementRequests") return `
    <s:Envelope

    xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">

  <s:Body>

    <s:Fault>

      <faultcode>s:Server.userException</faultcode>

      <faultstring>От сервера СУДМ 10.8.4.244:8010 на вызов GET-метода /api/material-movement/v1.0/material-movement-request получен пустой список materialMovementRequests</faultstring>

    </s:Fault>

  </s:Body>

</s:Envelope>
    `
    else if(param === "NoConnect") return `
    <s:Envelope

    xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">

  <s:Body>

    <s:Fault>

      <faultcode>s:Server.userException</faultcode>

      <faultstring>Hobo BFF не удается установить сетевое соединение с сервером СУДМ 10.8.4.244:8010 для вызова GET /api/material-movement/v1.0/stock</faultstring>

    </s:Fault>

  </s:Body>

</s:Envelope>
`
    else if(param === "NoRequest") return `
    <s:Envelope

    xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">

  <s:Body>

    <s:Fault>

      <faultcode>s:Server.userException</faultcode>

      <faultstring>Сервер СУДМ 10.8.4.244:8010 не ответил на вызов GET /api/material-movement/v1.0/stock в течение 20 секунд</faultstring>

    </s:Fault>

  </s:Body>

</s:Envelope>
    `
    else if(param === "ExtraException") return `
    <s:Envelope

    xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">

  <s:Body>

    <s:Fault>

      <faultcode>s:Server.userException</faultcode>

      <faultstring> Error in method "` + errCode + `": ` + ExtraException + `</faultstring>

    </s:Fault>

  </s:Body>

</s:Envelope>
`
}
