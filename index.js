/* global require */
const path = require('path');
var express = require('express');
var app = express();
var server = require('http').createServer(app);
var io = require('socket.io').listen(server);

const PORT = process.env.PORT || 8888;
var connectedClients = [];

server.listen(PORT);
console.log("Listening at port 8888..!!!");
app.use(express.static('public'));


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
io.on('connection', function (socket) {

	"use strict";
	connectedClients.push(socket);
	console.log('Made Socket Connection with id = ', socket.id);
	console.log('Current User = ' + connectedClients.length);

	//Disconnect
	socket.on('disconnect', function () {
		console.log('user disconnected');
		connectedClients.splice(connectedClients.indexOf(socket), 1);
		console.log('Current Active User = ' + connectedClients.length);
	});
	
	socket.on('IMAGE_DATA_FROM_STREAMER', data => {
        // send the base64 encoded frame to each connected ws
		socket.broadcast.emit('IMAGE_DATA_FOR_CLIENT', data);
				}
        );
});

