import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

PORT = 12345
BROADCAST_IP = '255.255.255.255'

# Set up UDP Broadcast
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', PORT))

# === Functions for UI ===

def get_username():
    """Creates a custom dialog to get the username."""
    username = ""

    def on_ok():
        nonlocal username
        username = entry.get()
        dialog.destroy()

    def on_close():
        nonlocal username
        username = "User"  # Default username if closed without input
        dialog.destroy()

    dialog = ttk.Toplevel(root)  # Use root as the parent
    dialog.title("Enter Username")
    dialog.geometry("300x150")
    dialog.resizable(False, False)
    dialog.protocol("WM_DELETE_WINDOW", on_close)  # Handle close button

    label = ttk.Label(dialog, text="Enter your username:", font=("Arial", 12))
    label.pack(pady=(20, 5))

    entry = ttk.Entry(dialog, width=25, font=("Arial", 12), bootstyle="dark")
    entry.pack(pady=5)
    entry.focus_set()  # Set focus to the entry box
    entry.bind("<Return>", lambda event: on_ok())  # Bind Enter key to on_ok

    ok_button = ttk.Button(dialog, text="OK", command=on_ok, bootstyle="success-outline")
    ok_button.pack(pady=(5, 20))

    dialog.wait_window()  # Wait for the dialog to close
    return username

# === UI with Ttkbootstrap ===

root = ttk.Window(themename="darkly")  # Use a modern theme
root.title("LAN Chat")
root.geometry("500x500") # Increase the size of the window
root.withdraw()  # Hide the main window initially

user_name = get_username()

root.deiconify() # Show the main window after get username

def receive_messages():
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            message = f"{addr[0]}: {data.decode()}"
            chat_box.config(state='normal')
            chat_box.insert(tk.END, f"{message}\n")
            chat_box.yview(tk.END)
            chat_box.config(state='disabled')
        except Exception as e:
            print("Error:", e)
            break

def send_message():
    msg = entry_box.get()
    if msg:
        sock.sendto(f"{user_name}: {msg}".encode(), (BROADCAST_IP, PORT))
        entry_box.delete(0, tk.END)

# Chat Box
chat_box = scrolledtext.ScrolledText(
    root,
    state='disabled',
    wrap=tk.WORD,
    width=50,
    height=15,
    bg="#2c2c2c",  # Dark background
    fg="white",    # White text
    insertbackground="white", # Cursor color
    font=("Arial", 11) # Change font size
)
chat_box.pack(padx=20, pady=20, fill=tk.BOTH, expand=True) # Add padding and expand

# Entry Box
entry_box = ttk.Entry(
    root,
    width=35,
    bootstyle="dark",
    font=("Arial", 11) # Change font size
)
entry_box.pack(side=tk.LEFT, padx=(20, 0), pady=(0, 20), fill=tk.X, expand=True) # Add padding and expand
entry_box.bind("<Return>", lambda event: send_message())

# Create a custom style for the button
style = ttk.Style()
style.configure("TButton", font=("Arial", 11))  # Set the font here

# Send Button
send_button = ttk.Button(
    root,
    text="Send",
    command=send_message,
    style="TButton",  # Apply the custom style
    bootstyle="success" # Change bootstyle
)
send_button.pack(side=tk.LEFT, padx=20, pady=(0, 20)) # Add padding

# Start the thread for receiving messages
recv_thread = threading.Thread(target=receive_messages, daemon=True)
recv_thread.start()

root.mainloop()
