from picarx import Picarx
import socket
import os

HOST = "192.168.1.192"  # raspberry pi IP
PORT = 65432           # port

power_val = 50
direction = ""

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print("server started and listening...")

    try:
        px = Picarx()
        temp = os.popen("vcgencmd measure_temp").readline()
        temp_val = temp.replace("temp=", "").replace("'C\n", "")
        while True:
            client, client_info = s.accept()
            print("connected to:", client_info)

            try:
                data = client.recv(1024).decode()
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
                    px.forward(0)
                elif data == "status":
                    status = {
                        "direction": direction,
                        "speed": power_val,
                        "distance": 0.0,
                        "temperature": temp_val,
                    }
                    client.sendall(str(status).encode())
                else:
                    client.sendall(f"unknown command: {data}".encode())
                status = {
                    "direction": direction,
                    "speed": power_val,
                    "distance": 0.0,
                    "temperature": temp_val,
                }
                client.sendall(str(status).encode())
                print(f"executed command: {data}")

            except Exception as e:
                print(f"error handling client: {e}")
            finally:
                client.close()

    except KeyboardInterrupt:
        print("server interrupted, stopping car...")
        px.forward(0)
    finally:
        px.forward(0)
        print("server closed, car stopped.")
