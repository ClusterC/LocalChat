import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

HOST = '127.0.0.1'
PORT = 9999

# สร้างการเชื่อมต่อกับ server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# ฟังก์ชันรับข้อความจาก server
def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode()
            if message:
                chat_box.config(state='normal')  # เปิดการแก้ไขข้อความใน chat box
                chat_box.insert(tk.END, message + '\n')  # แสดงข้อความที่ได้รับ
                chat_box.yview(tk.END)  # เลื่อนหน้าจอไปที่ข้อความล่าสุด
                chat_box.config(state='disabled')  # ปิดการแก้ไขข้อความ
        except:
            print("An error occurred.")
            client.close()
            break

# ฟังก์ชันส่งข้อความไปยัง server
def send_message():
    message = entry_box.get()
    if message:
        client.send(message.encode())  # ส่งข้อความที่พิมพ์ไปยัง server
        entry_box.delete(0, tk.END)  # ลบข้อความที่พิมพ์ออกจาก entry box

# สร้างหน้าต่าง UI
root = tk.Tk()
root.title("Chat Client")

# กำหนดขนาดหน้าต่าง
root.geometry("400x400")

# สร้างพื้นที่แสดงข้อความแชท
chat_box = scrolledtext.ScrolledText(root, state='disabled', wrap=tk.WORD, width=50, height=15, font=("Arial", 10))
chat_box.pack(padx=10, pady=10)

# สร้างกล่องข้อความสำหรับพิมพ์ข้อความ
entry_box = tk.Entry(root, width=35, font=("Arial", 12))
entry_box.pack(side=tk.LEFT, padx=(10,0), pady=(0,10))
entry_box.bind("<Return>", lambda event: send_message())  # ส่งข้อความเมื่อกด Enter

# สร้างปุ่มส่งข้อความ
send_button = tk.Button(root, text="Send", command=send_message, font=("Arial", 12))
send_button.pack(side=tk.LEFT, padx=10, pady=(0,10))

# เริ่ม thread สำหรับรับข้อความจาก server
threading.Thread(target=receive_messages, daemon=True).start()

# เริ่มทำงานของ UI
root.mainloop()
