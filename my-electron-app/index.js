document.getElementById("myButton").addEventListener("click", greeting);
var server_port = 65432;
var server_addr = "192.168.1.192"; // the IP address of your Raspberry Pi
//var server_addr = process.env.IP_ADDRESS_PI;
console.log(server_addr)

function client(){
    const net = require('net');
    var input = document.getElementById("myName").value;

    const client = net.createConnection({ port: server_port, host: server_addr}, () => {
        // 'connect' listener.
        console.log('connected to server!');
        //send the message
        client.write(`${input}\r\n`)
    });

    //get the data from the server
    client.on('data', (data) => {
        document.getElementById("greet_from_server").innerHTML = data;
        console.log(data.toString());
        client.end();
        client.destroy();
    });

    client.on('end', () => {
        console.log('disconnected from server')
    });
}

function greeting(){
    var name = document.getElementById("myName").value;
    document.getElementById("greet").innerHTML = "Hello " + name + " !";
//    to_server(name);
    client();
}