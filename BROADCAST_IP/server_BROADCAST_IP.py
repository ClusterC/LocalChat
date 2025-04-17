import socket
import threading
import random
import os,sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

from os import system
from ascii_magic import AsciiArt

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

PORT = 12345
BROADCAST_IP = '255.255.255.255'
# ตั้งค่าการรับ-ส่ง UDP Broadcast
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', PORT))

# รายชื่อผู้ใช้
clients = {}

# ฟังก์ชันสำหรับรับข้อความจาก client
def handle_client(addr):
    try:
        while True:
            data, _ = sock.recvfrom(1024)
            message = data.decode()
            print(f"Message from {addr[0]}: {message}")
            # ส่งข้อความไปยังทุกคนในวง LAN
            broadcast_message(message)
    except Exception as e:
        print(f"Error with client {addr[0]}: {e}")
        del clients[addr]

# ฟังก์ชันสำหรับส่งข้อความไปยังทุกคนในวง LAN
def broadcast_message(message):
    for client_addr in clients.values():
        sock.sendto(message.encode(), client_addr)

# เริ่มต้นการรับการเชื่อมต่อจาก client
def accept_clients():
    while True:
        data, addr = sock.recvfrom(1024)
        # เช็คชื่อผู้ใช้
        user_info = data.decode().split(": ")
        username = user_info[0]
        if addr not in clients:
            clients[addr] = (username, random.choice(["#FF5733", "#33FF57", "#3357FF", "#F033FF"]))  # สีสุ่ม
            print(f"New user connected: {username} ({addr[0]})")
            threading.Thread(target=handle_client, args=(addr,), daemon=True).start()

accept_clients_thread = threading.Thread(target=accept_clients, daemon=True)
accept_clients_thread.start()


# Server อยู่ใน loop ตลอดเวลา
run()
print("Server is running...")
while True:
    pass  # Server ทำงานตลอดเวลา
