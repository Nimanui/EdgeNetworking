import picar_4wd as fc
import socket

HOST = "192.168.0.10"  # raspberry pi IP
PORT = 65432           # port

power_val = 50
direction = ""

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print("server started and listening...")

    try:
        while True:
            client, client_info = s.accept()
            print("connected to:", client_info)

            try:
                data = client.recv(1024).decode()
                if data == "forward":
                    direction = "forward"
                    fc.forward(power_val)
                elif data == "backward":
                    direction = "backward"
                    fc.backward(power_val)
                elif data == "left":
                    direction = "left"
                    fc.turn_left(power_val)
                elif data == "right":
                    direction = "right"
                    fc.turn_right(power_val)
                elif data == "stop":
                    direction = "stop"
                    fc.stop()
                elif data == "status":
                    status = {
                        "direction": direction,
                        "speed": power_val,
                        "distance": 0.0,
                        "temperature": 0.0
                    }
                    client.sendall(str(status).encode())
                else:
                    client.sendall(f"unknown command: {data}".encode())

                print(f"executed command: {data}")

            except Exception as e:
                print(f"error handling client: {e}")
            finally:
                client.close()

    except KeyboardInterrupt:
        print("server interrupted, stopping car...")
        fc.stop()
    finally:
        fc.stop()
        print("server closed, car stopped.")
