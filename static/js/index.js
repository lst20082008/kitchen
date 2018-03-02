console.log("index!!!");
var socket = io.connect('http://' + document.domain + ':' + location.port+'/ioconnect');
console.log("connected");
document.getElementById('warning').remove();
function add(name){
    socket.emit('add',name);
    console.log('add',name);
}
function reduce(name){
    socket.emit('reduce',name);
    console.log('reduce',name);
}
socket.on('update',function(message){
    console.log(message);
    message = JSON.parse(message);
    console.log(message);
    document.getElementById(message.name+'num').innerHTML = message.num;
})