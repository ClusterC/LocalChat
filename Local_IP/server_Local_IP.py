import socket
import os,sys
from os import system
from ascii_magic import AsciiArt

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def set_cmd_size(columns, lines):
    system(f'mode con: cols={columns} lines={lines}')

def run():
    set_cmd_size(151, 25)
    print('\n')
    try:
        my_art = AsciiArt.from_image(resource_path('logo.png'))
        my_art.to_terminal(columns=150)
    except:
        pass
    print(f'{'POWER BY CLUSTER C':>149}')
run()

PORT = 12345
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.bind(('', PORT))

clients = {}  # addr → username

print("Server is running...")

while True:
    try:
        data, addr = sock.recvfrom(1024)
        message = data.decode()

        if addr not in clients:
            username = message.split(": ")[0]
            clients[addr] = username
            print(f"New user connected: {username} ({addr[0]})")
        else:
            print(f"Message from {clients[addr]} ({addr[0]}): {message}")

        # ส่งต่อ message ให้ client คนอื่นทั้งหมด
        for client_addr in clients:
            sock.sendto(message.encode(), client_addr)

    except Exception as e:
        print("Error:", e)