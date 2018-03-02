console.log("main!!!");
var socket = io.connect('http://' + document.domain + ':' + location.port+'/ioconnect');
console.log("connected");
function send(){
    socket.emit('send',{'data':document.getElementById('toSend').value});
    console.log('send',{'data':document.getElementById('toSend').value});
}
socket.on('return',function(message){
    var li = document.createElement('li');
    li.innerHTML = message;
    console.log(li);
    document.getElementById("mainDiv").appendChild(li);
})