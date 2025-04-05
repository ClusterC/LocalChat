# chat_client.py
import socket
import threading

HOST = '127.0.0.1'
PORT = 9999

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode()
            if message:
                print(message)
        except:
            print("An error occurred.")
            client.close()
            break

def send_messages():
    while True:
        message = input()
        client.send(message.encode())

threading.Thread(target=receive_messages).start()
send_messages()