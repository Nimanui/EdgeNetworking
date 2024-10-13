document.onkeydown = updateKey;
document.onkeyup = resetKey;

var server_port = 65432;
var server_addr = "192.168.1.134";

function parse_payload(payload) {
    var components = JSON.parse(payload.toString())
    return components
}

function client() {

    const net = require('net');
    var input = document.getElementById("myName").value;
    var secretInput = document.getElementById("hiddenItem").value;
    console.log(secretInput)

    const client = net.createConnection({ port: server_port, host: server_addr }, () => {
        // Connect listener
        console.log("Connected to Server")
        client.write(`${secretInput}\r\n`)
    });

    client.on('data', (data) => {
        console.log(data.toString());
        var payload = parse_payload(data);
        document.getElementById("greet_from_server").innerHTML = "Received " + data + " ?";
        for (const key in payload) {
            document.getElementById(key).innerHTML = payload[key]
        }

        client.end();
        client.destroy();
    });

    client.on('end', () => {
        console.log("Disconnected from server");
    });

}


// for detecting which key is been pressed W,A,S,D
function updateKey(e) {

    e = e || window.event;

    if (e.keyCode == '87') {
        // up (w)
        document.getElementById("upArrow").style.color = "green";
        document.getElementById("hiddenItem").value = "forward";
    }
    else if (e.keyCode == '83') {
        // down (s)
        document.getElementById("downArrow").style.color = "green";
        document.getElementById("hiddenItem").value = "backward";
        greeting();
        //send_data("83");
    }
    else if (e.keyCode == '65') {
        // left (a)
        document.getElementById("leftArrow").style.color = "green";
        document.getElementById("hiddenItem").value = "left";
    }
    else if (e.keyCode == '68') {
        // right (d)
        document.getElementById("rightArrow").style.color = "green";
        document.getElementById("hiddenItem").value = "right";
    }
}

// reset the key to the start state 
function resetKey(e) {

    e = e || window.event;

    document.getElementById("upArrow").style.color = "grey";
    document.getElementById("downArrow").style.color = "grey";
    document.getElementById("leftArrow").style.color = "grey";
    document.getElementById("rightArrow").style.color = "grey";

    document.getElementById("hiddenItem").value = "stop";
}

function update_data() {
    setInterval(function () {
        client();
    }, 100);
}

function greeting() {
    // Get the element from HTML
    var name = document.getElementById("myName").value;
    //Update the content in HTML
    document.getElementById("greet").innerHTML = "Hello " + name + " !";
    client();
}