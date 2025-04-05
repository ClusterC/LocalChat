# chat_server.py
import socket
import threading

HOST = '0.0.0.0'
PORT = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []

def broadcast(message, sender_conn):
    for client in clients:
        if client != sender_conn:
            try:
                client.send(message)
            except:
                clients.remove(client)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    clients.append(conn)
    
    # Notify other clients about new user
    broadcast(f"New user joined: {addr}\n".encode(), conn)
    
    while True:
        try:
            msg = conn.recv(1024)
            if msg:
                # Broadcast message to other clients
                broadcast(msg, conn)
        except:
            # Client disconnected
            print(f"[DISCONNECT] {addr} disconnected.")
            clients.remove(conn)
            conn.close()
            # Notify others about the disconnection
            broadcast(f"User {addr} has left the chat.\n".encode(), conn)
            break

print(f"[STARTING] Server is listening on {HOST}:{PORT}")
while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()