/* global require */
const path = require('path');
var express = require('express');
var app = express();
var httpServer = require('http').createServer(app);
const WebSocket = require('ws');
const wsServer = new WebSocket.Server({ server: httpServer }, () => console.log(`WS server is listening at ws://localhost:${WS_PORT}`));
const PORT = process.env.PORT || 8888;
var connectedClients = [];


httpServer.listen(PORT, () => console.log(`HTTP server listening at http://localhost:${PORT}`));


app.get('/client', (req, res) => res.sendFile(path.resolve(__dirname, './public/client.html'))
	   );
app.get('/streamer', (req, res) => res.sendFile(path.resolve(__dirname, './public/streamer.html'))
	   );
app.get('/', (req, res) => {
	res.send(`
        <a href="streamer">Streamer</a><br>
        <a href="client">Client</a>
    `);
});

wsServer.on('connection', (ws, req) => {
    console.log('Connected');
    // add new connected client
    connectedClients.push(ws);
    // listen for messages from the streamer, the clients will not send anything so we don't need to filter
    ws.on('message', data => {
        // send the base64 encoded frame to each connected ws
        connectedClients.forEach((ws, i) => {
            if (ws.readyState === ws.OPEN) { // check if it is still connected
                ws.send(data); // send
            } else { // if it's not connected remove from the array of connected ws
                connectedClients.splice(i, 1);
            }
        });
    });
});

