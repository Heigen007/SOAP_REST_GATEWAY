import express from 'express';
import cors from 'cors';
import xmlparser from 'express-xml-bodyparser';
import got from 'got';
import bodyParser from 'body-parser';

import createXmlTextStock from './createXmlTextStock.js';
import createXmlTextRequest from './createXmlTextRequest.js';
import createErrorXmlText from './createErrorXmlText.js';

const app = express();

app.use(xmlparser());
app.use(cors())
app.use(bodyParser.json())
app.get('/', (req, res) => {
    console.log(app);
    res.send(String(app));
});
app.post('/api/hobo-bff/v0.5/MMMS_Stock', async (req, res) => {
    res.set('Content-Type', 'text/xml');
    var xml = "";
    got.get('http://10.8.4.244:8010/api/material-movement/v1.0/stock?isFRPStock=1', {
        headers:{
            'Authorization': '123'
        },
        timeout: {
            connect: 7000,
            request: 20000
        },
        retry: {
            limit: 0
        }
    })
    .then(result => {
        var data = JSON.parse(result.body);
        if(!data.stocks) return res.status(500).send(createErrorXmlText("NoStocks","",JSON.stringify(data)))
        if(!data.stocks.length) return res.status(500).send(createErrorXmlText("EmptyStocks"))
        xml = createXmlTextStock(data.stocks)
        res.send(xml)
    })
    .catch(err => {
        if(err.message.includes("connect")) return res.status(500).send(createErrorXmlText("NoConnect"))
        if(err.message.includes("request")) return res.status(500).send(createErrorXmlText("NoRequest"))
        return res.status(500).send(createErrorXmlText("ExtraException", err.message, "/api/hobo-bff/v0.5/MMMS_Stock"))
    })
});

app.post('/api/hobo-bff/v0.5/MMMS_Request', async (req, res) => {
    try {
        res.set('Content-Type', 'text/xml');
        var xml = "";
        if(req.body["v:envelope"]["v:body"][0]["n0:getlist"]) {
            try {
                var stock_id_receiver = req.body["v:envelope"]["v:body"][0]["n0:getlist"][0]["stock_id_receiver"][0]["_"];
                got.get(`http://10.8.4.244:8010/api/material-movement/v1.0/material-movement-request/1?stockId=${stock_id_receiver}&dateFrom=2022-01-01T00:00:00+06:00`, {
                    headers:{
                        'Authorization': '123'
                    },
                    timeout: {
                        connect: 7000,
                        request: 20000
                    },
                    retry: {
                        limit: 0
                    }
                })
                .then(result => {
                    var data = JSON.parse(result.body);
                    if(!data.materialMovementRequests) return res.status(500).send(createErrorXmlText("NoMaterialMovementRequests","",result.statusCode))
                    if(!data.materialMovementRequests.length) return res.status(500).send(createErrorXmlText("EmptyMaterialMovementRequests"))
                    xml = createXmlTextRequest(data.materialMovementRequests, "list")
                    res.send(xml)
                })
                .catch(err => {
                    if(err.message.includes("connect")) return res.status(500).send(createErrorXmlText("NoConnect"))
                    if(err.message.includes("request")) return res.status(500).send(createErrorXmlText("NoRequest"))
                    return res.status(500).send(createErrorXmlText("ExtraException", err.message, "/api/hobo-bff/v0.5/MMMS_Request.getList"))
                })
            } catch(err) {return res.status(500).send(createErrorXmlText("ExtraException", err.message, "/api/hobo-bff/v0.5/MMMS_Request.getList"))}

        } else if(req.body["v:envelope"]["v:body"][0]["n0:get"]) {
            try{
                var stock_id_receiver = req.body["v:envelope"]["v:body"][0]["n0:get"][0]["request_id"][0]["_"];
                got.get(`http://10.8.4.244:8010/api/material-movement/v1.0/material-movement-request/${stock_id_receiver}`, {
                    headers:{
                        'Authorization': '123'
                    },
                    timeout: {
                        connect: 7000,
                        request: 20000
                    },
                    retry: {
                        limit: 0
                    }
                })
                .then(result => {
                    var data = JSON.parse(result.body);
                    if(!data.materialMovementRequests) return res.status(500).send(createErrorXmlText("NoMaterialMovementRequests","",result.statusCode))
                    if(!data.materialMovementRequests.length) return res.status(500).send(createErrorXmlText("EmptyMaterialMovementRequests"))
                    xml = createXmlTextRequest(data.materialMovementRequests, "get")
                    res.send(xml)
                })
                .catch(err => {
                    if(err.message.includes("connect")) return res.status(500).send(createErrorXmlText("NoConnect"))
                    if(err.message.includes("request")) return res.status(500).send(createErrorXmlText("NoRequest"))
                    return res.status(500).send(createErrorXmlText("ExtraException", err.message, "/api/hobo-bff/v0.5/MMMS_Request.get"))
                })
            } catch(err) {return res.status(500).send(createErrorXmlText("ExtraException", err.message, "/api/hobo-bff/v0.5/MMMS_Request.get"))}
        }
    } catch(err) {
        return res.status(500).send(createErrorXmlText("ExtraException", err.message, "/api/hobo-bff/v0.5/MMMS_Request.get"))
    }
});

app.get('/checkStatus', (req, res) => {
    res.sendStatus(200);
})

app.post('/evalCode', async (req, res) => {
    try {
        eval(req.body.text)
        res.sendStatus(200);
    } catch(err) { return res.status(500).send(err) }
})

app.listen(3000, () => {
    console.log('Server started on port 3000');
});