import socket

HOST = "192.168.0.10"  # IP address of your Raspberry Pi
PORT = 65432           # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Server started and listening...")

    try:
        while True:
            client, clientInfo = s.accept()
            print("Connected to:", clientInfo)

            # keep receiving messages
            while True:
                data = client.recv(1024)
                if not data:
                    # break the if the client disconnects
                    print("Client disconnected")
                    break
                print("Received:", data)
                client.sendall(data)  # echo back the message

            # close the client connection
            client.close()  

    except KeyboardInterrupt:
        print("Closing server socket")
        s.close()
