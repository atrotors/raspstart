var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);

io.on('connection', function(socket){
  socket.on('power_button', function(status){
    if (status == 'true') {
      io.emit('LED', 'on');
    } else if (status == 'false') {
      io.emit('LED', 'off');
    }
  });
});

http.listen(3000, function(){});
