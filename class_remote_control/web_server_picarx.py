from picarx import Picarx
import socket

HOST = "192.168.1.192"  # raspberry pi IP
PORT = 65432           # port

power_val = 50

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("server started and listening...")

    try:
        px = Picarx()
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
                        direction = "forward"
                        px.set_dir_servo_angle(0)
                        px.forward(power_val)
                    elif data == "backward":
                        direction = "backward"
                        px.set_dir_servo_angle(0)
                        px.backward(power_val)
                    elif data == "left":
                        direction = "left"
                        px.set_dir_servo_angle(-30)
                        px.forward(power_val)
                    elif data == "right":
                        direction = "right"
                        px.set_dir_servo_angle(30)
                        px.forward(power_val)
                    elif data == "stop":
                        direction = "stop"
                        px.stop()
                    elif data == "status":
                        # todo : implement distance and temperature.
                        status = {
                            "direction": "forward",
                            "speed": power_val,
                            "distance": 0.0,
                            "temperature": 0.0
                        }
                        client.sendall(str(status).encode())
                    else:
                        # handle unknown commands
                        client.sendall(f"unknown command: {data}".encode())

                    print(f"executed command: {data}")

    except KeyboardInterrupt:
        print("server interrupted, stopping car...")
        px.stop()
    finally:
        px.stop()
        print("server closed, car stopped.")
