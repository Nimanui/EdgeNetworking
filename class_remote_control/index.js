document.onkeydown = updateKeyBoth;
document.onkeyup = resetKey;

var server_port = 65432;
var server_addr = "192.168.1.192";   // the IP address of your Raspberry PI

// send commands to the raspberry pi server
function sendCommand(command) {
    
    console.log(`connecting to server at ${server_addr}:${server_port}`);
    const net = require('net');

    const client = net.createConnection({ port: server_port, host: server_addr }, () => {
        console.log(`connected to server, sending command: ${command}`);
        client.write(command);
    });

    client.on('data', (data) => {
        const response = data.toString();
        
        if (command.length > 0) {

            try {
                const jsonData = JSON.parse(response.replace(/'/g, '"'));

                document.getElementById("direction").innerText = jsonData.direction;
                document.getElementById("speed").innerText = jsonData.speed;
                document.getElementById("temperature").innerText = jsonData.temperature + "°C";
            } catch (e) {
                alert(e)
                document.getElementById("bluetooth").innerText = response;
            }
        }
        client.end();
    });

    client.on('error', (err) => {
        console.error(`connection error: ${err.message}`);
    });
    
}

// for detecting which key is been pressed w,a,s,d,q
function updateKey(e) {
    e = e || window.event;
    console.log(e.keyCode)
    if (e.keyCode === 38) { // up arrow
        document.getElementById("upArrow").style.color = "green";
        sendCommand("forward");
    } else if (e.keyCode === 40) { // down arrow
        document.getElementById("downArrow").style.color = "green";
        sendCommand("backward");
    } else if (e.keyCode === 37) { // left arrow
        document.getElementById("leftArrow").style.color = "green";
        sendCommand("left");
    } else if (e.keyCode === 39) { // right arrow
        document.getElementById("rightArrow").style.color = "green";
        sendCommand("right");
    } else if (e.keyCode === 81) { // q key for stop
        sendCommand("stop");
    }
}

// for detecting which key is been pressed w,a,s,d,q
function updateKeyBoth(e) {
    e = e || window.event;
    console.log(e.keyCode)
    if (e.keyCode === 87 || e.keyCode === 38) { // up arrow
        document.getElementById("upArrow").style.color = "green";
        sendCommand("forward");
    } else if (e.keyCode === 83 || e.keyCode === 40) { // down arrow
        document.getElementById("downArrow").style.color = "green";
        sendCommand("backward");
    } else if (e.keyCode === 65 || e.keyCode === 37) { // left arrow
        document.getElementById("leftArrow").style.color = "green";
        sendCommand("left");
    } else if (e.keyCode === 68 || e.keyCode === 39) { // right arrow
        document.getElementById("rightArrow").style.color = "green";
        sendCommand("right");
    } else if (e.keyCode === 81) { // q key for stop
        sendCommand("stop");
    } else if (e.keyCode === 84) { // up camera t
        sendCommand("upCamera");
    } else if (e.keyCode === 71) { // down camera g
        sendCommand("downCamera");
    } else if (e.keyCode === 70) { // left camera f
        sendCommand("leftCamera");
    } else if (e.keyCode === 72) { // right camera h
        sendCommand("rightCamera");
    } else if (e.keyCode === 90) { // start camera z
        document.getElementById("cameraFeed").src = "http://" + server_addr +":9000/mjpg"
//        document.getElementById("cameraFeed2").source = "http://" + server_addr +":9000/mjpg"
        sendCommand("startCamera");
    } else if (e.keyCode === 88) { // stop camera x
        sendCommand("stopCamera");
    } else if (e.keyCode === 80) { // stop camera x
        sendCommand("takePhoto");
    }
}

// reset the key to the start state 
function resetKey(e) {
    e = e || window.event;

    document.getElementById("upArrow").style.color = "grey";
    document.getElementById("downArrow").style.color = "grey";
    document.getElementById("leftArrow").style.color = "grey";
    document.getElementById("rightArrow").style.color = "grey";
    
    const movementKeys = [37, 38, 39, 40, 87, 83, 65, 68, 84, 71, 70, 72, 90, 88];
    if (movementKeys.includes(e.keyCode)) { 
        sendCommand("stop")
    }
    
}

// handle the submit button
document.getElementById("submit").addEventListener("click", () => {
    const message = document.getElementById("message").value;
    sendCommand(message);
    document.getElementById("message").value = ""; // clear the text box
});

// optional - update data at intervals
function updateData() {
    setInterval(function(){
        sendCommand("status");
    }, 5000); // adjust interval
}
