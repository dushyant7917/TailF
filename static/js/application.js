$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');

    //receive details from server
    socket.on('newnumber', function(msg) {
        console.log(typeof(msg.number))
        $('#log').append('<br>' + $('<div/>').text(msg.number).html());
    });

    socket.on('my_response', function(msg) {
        $('#log').append('<br>' + $('<div/>').text(msg.data).html());
    });

});
