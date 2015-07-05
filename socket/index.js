var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);

var state;

io.on('connection', function(socket){
  if(state)
    socket.emit('LED', state);

  socket.on('power_button', function(status){
    if (status == 'true') {
      io.emit('LED', 'on');
      state = 'on';
    } else if (status == 'false') {
      io.emit('LED', 'off');
      state = 'off';
    }
  });
});

http.listen(3000, function(){});
