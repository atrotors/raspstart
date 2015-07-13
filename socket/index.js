var http = require('http');
var server = http.createServer().listen(3000, '127.0.0.1');
var io = require('socket.io').listen(server);
var redis = require("redis"),
client = redis.createClient();
client.subscribe('fuse.socketio')

var state;

io.on('connection', function(socket){
  if(state)
    socket.emit('LED', state);

  socket.on('power_button', function(status){
    if (status == 'true') {
      socket.broadcast.emit('LED', 'on');
      state = 'on';
    } else if (status == 'false') {
      socket.broadcast.emit('LED', 'off');
      state = 'off';
    }
  });
});

client.on('message', function(chnl, msg) {
  console.log('redis msg: ', msg);
  io.emit('history-recieved', msg)
});
