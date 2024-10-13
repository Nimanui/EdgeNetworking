import socket
from picar_interface import Picar_Tracker


HOST = "192.168.1.134"
PORT = 65432

TRACKER = Picar_Tracker()
ACCEPTABLE_COMMANDS = ["forward", "backward", "left", "right", "stop"]

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        try:
            while 1:
                client, clientInfo = s.accept()
                print(f"Server recv from: {clientInfo}")
                data = client.recv(1024)
                if data != b"":
                    print(data)
                    decoded_data = data.decode("utf-8").strip()
                    if (decoded_data in ACCEPTABLE_COMMANDS):
                        print(f"Got Keyboard command: {decoded_data}")
                        TRACKER.parse_movement(decoded_data)
                    json_payload = TRACKER.generate_payload()
                    client.sendall(json_payload)
        except:
            print("Closing socket")
            client.close()
            s.close()

if __name__ == "__main__":
    main()