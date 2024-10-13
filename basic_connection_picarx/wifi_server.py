from picarx import Picarx
import socket
import os
from vilib import Vilib
from time import sleep, time, strftime, localtime

HOST = "192.168.1.192"  # raspberry pi IP
PORT = 65432           # port

power_val = 50
direction = ""
user = os.getlogin()
user_home = os.path.expanduser(f'~{user}')
camera_pan = 0
camera_tilt = 0

def take_photo():
    _time = strftime('%Y-%m-%d-%H-%M-%S',localtime(time()))
    name = 'photo_%s'%_time
    path = f"{user_home}/Pictures/picar-x/"
    Vilib.take_photo(name, path)
    print('\nphoto save as %s%s.jpg'%(path,name))


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
                elif data == "startCamera":
                    Vilib.camera_start(vflip=False, hflip=False)
                    Vilib.display(local=True, web=True)
                    px.set_cam_tilt_angle(0)
                    px.set_cam_pan_angle(0)
                elif data == "stopCamera":
                    Vilib.camera_close()
                elif data == "takePhoto":
                    take_photo()
                elif data == "upCamera":
                    camera_tilt = min(65, max(-35, camera_tilt + 10))
                    px.set_cam_tilt_angle(camera_tilt)
                elif data == "downCamera":
                    camera_tilt = min(65, max(-35, camera_tilt - 10))
                    px.set_cam_tilt_angle(camera_tilt)
                elif data == "leftCamera":
                    camera_pan = min(90, max(-90, camera_pan - 10))
                    px.set_cam_pan_angle(camera_pan)
                elif data == "rightCamera":
                    camera_pan = min(90, max(-90, camera_pan + 10))
                    px.set_cam_pan_angle(camera_pan)
                elif data == "status":
                    status = {
                        "direction": direction,
                        "speed": power_val,
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

