import picar_4wd as fc
import socket

HOST = "192.168.0.10"  # raspberry pi IP
PORT = 65432           # port

power_val = 50

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
                    distance = fc.get_distance_at(0)
                    temp = fc.cpu_temperature()
                    status = {
                        "direction": "forward",
                        "speed": power_val,
                        "distance": distance,
                        "temperature": temp
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
