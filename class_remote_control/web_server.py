import picar_4wd as fc
import socket

HOST = "192.168.0.10"  # raspberry pi IP
PORT = 65432           # port

power_val = 50

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("server started and listening...")

    try:
        while True:
            client, _ = s.accept()
            with client:
                print("client connected")
                while True:
                    data = client.recv(1024).decode()
                    if not data:
                        print("client disconnected")
                        break
                    if data == "forward":
                        fc.forward(power_val)
                    elif data == "backward":
                        fc.backward(power_val)
                    elif data == "left":
                        fc.turn_left(power_val)
                    elif data == "right":
                        fc.turn_right(power_val)
                    elif data == "stop":
                        fc.stop()
                    elif data == "status":
                        # todo : implement distance and temperature.
                        status = {
                            "direction": "forward",
                            "speed": power_val,
                            "distance": 0.0,
                            "temperature": fc.cpu_temperature()
                        }
                        client.sendall(str(status).encode())
                    else:
                        # handle unknown commands
                        client.sendall(f"unknown command: {data}".encode())

                    print(f"executed command: {data}")

    except KeyboardInterrupt:
        print("server interrupted, stopping car...")
        fc.stop()
    finally:
        fc.stop()
        print("server closed, car stopped.")
