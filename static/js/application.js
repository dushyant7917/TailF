$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');

    //receive details from server
    socket.on('newnumber', function(msg) {
        console.log(type(msg.number))
        $('#log').append('<br>' + $('<div/>').text(msg.number).html());
    });

});
