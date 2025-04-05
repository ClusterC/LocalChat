import socket
import threading
import random

PORT = 12345
BROADCAST_IP = '255.255.255.255'

# ตั้งค่าการรับ-ส่ง UDP Broadcast
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', PORT))

# รายชื่อผู้ใช้และสี
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
        # เช็คชื่อผู้ใช้และสี
        user_info = data.decode().split(": ")
        username = user_info[0]
        if addr not in clients:
            clients[addr] = (username, random.choice(["#FF5733", "#33FF57", "#3357FF", "#F033FF"]))  # สีสุ่ม
            print(f"New user connected: {username} ({addr[0]})")
            threading.Thread(target=handle_client, args=(addr,), daemon=True).start()

accept_clients_thread = threading.Thread(target=accept_clients, daemon=True)
accept_clients_thread.start()

# Server อยู่ใน loop ตลอดเวลา
print("Server is running...")
while True:
    pass  # Server ทำงานตลอดเวลา
