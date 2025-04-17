import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import sys # Import sys to exit if IP window is closed

PORT = 12345
# SERVER_IP = 'localhost'  # ← Remove hardcoded IP

# Initialize SERVER_IP, will be set by get_server_ip()
SERVER_IP = None

# === Functions for UI ===

def get_server_ip():
    """Creates a dialog window to get the Server IP address."""
    server_ip_input = ""
    def on_ok():
        nonlocal server_ip_input
        ip_input = entry.get().strip()
        # Basic validation (optional, can be more robust)
        if ip_input:
            server_ip_input = ip_input
            dialog.destroy()
        else:
            # Optionally show an error or just keep the dialog open
            print("Please enter a valid IP address or hostname.")


    def on_close():
        """Exits the application if the IP dialog is closed."""
        print("IP address input cancelled. Exiting.")
        root.destroy() # Destroy the main hidden window
        sys.exit() # Exit the script

    dialog = ttk.Toplevel(root)
    dialog.title("Enter Server IP")
    dialog.geometry("300x150")
    dialog.resizable(False, False)
    dialog.protocol("WM_DELETE_WINDOW", on_close) # Handle closing the dialog

    label = ttk.Label(dialog, text="Enter the Server IP address:", font=("Arial", 12))
    label.pack(pady=(20, 5))

    entry = ttk.Entry(dialog, width=25, font=("Arial", 12), bootstyle="dark")
    entry.insert(0, "localhost") # Default value
    entry.pack(pady=5)
    entry.focus_set()
    entry.bind("<Return>", lambda event: on_ok())

    ok_button = ttk.Button(dialog, text="OK", command=on_ok, bootstyle="success-outline")
    ok_button.pack(pady=(5, 20))

    dialog.wait_window() # Wait for this dialog to close
    return server_ip_input

def get_username():
    """Creates a dialog window to get the Username."""
    username = ""
    def on_ok():
        nonlocal username
        name_input = entry.get().strip()
        username = name_input if name_input else "User"
        dialog.destroy()

    def on_close():
        """Exits the application if the username dialog is closed."""
        print("Username input cancelled. Exiting.")
        root.destroy()
        sys.exit()

    dialog = ttk.Toplevel(root)
    dialog.title("Enter Username")
    dialog.geometry("300x150")
    dialog.resizable(False, False)
    dialog.protocol("WM_DELETE_WINDOW", on_close) # Handle closing the dialog

    label = ttk.Label(dialog, text="Enter your username:", font=("Arial", 12))
    label.pack(pady=(20, 5))

    entry = ttk.Entry(dialog, width=25, font=("Arial", 12), bootstyle="dark")
    entry.pack(pady=5)
    entry.focus_set()
    entry.bind("<Return>", lambda event: on_ok())

    ok_button = ttk.Button(dialog, text="OK", command=on_ok, bootstyle="success-outline")
    ok_button.pack(pady=(5, 20))

    dialog.wait_window() # Wait for this dialog to close
    return username

# === UI with Ttkbootstrap ===

root = ttk.Window(themename="darkly")
root.title("LAN Chat")
root.geometry("500x500")
root.withdraw() # Keep main window hidden initially

# --- Get Server IP first ---
SERVER_IP = get_server_ip()
if not SERVER_IP: # Exit if get_server_ip returned empty (shouldn't happen with current on_close)
    print("No Server IP provided. Exiting.")
    sys.exit()

# --- Then get Username ---
user_name = get_username()
if not user_name: # Exit if get_username returned empty
    print("No username provided. Exiting.")
    sys.exit()

# --- Now show the main window ---
root.title(f"LAN Chat - {user_name} @ {SERVER_IP}") # Update title
root.deiconify()

# === Socket Setup (moved after getting IP) ===
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 0))  # Bind to any available port on the client side
except socket.error as e:
    print(f"Failed to create or bind socket: {e}")
    # Optionally show an error message in the UI
    tk.messagebox.showerror("Socket Error", f"Failed to initialize network socket:\n{e}")
    root.destroy()
    sys.exit()


# === Network Functions ===

def receive_messages():
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            # Optional: Check if the message is from the expected server IP
            # if addr[0] != SERVER_IP:
            #     print(f"Ignored message from unexpected source: {addr}")
            #     continue
            message = data.decode('utf-8') # Specify encoding
            # Update UI safely from the main thread
            root.after(0, update_chat_box, message)
        except socket.error as e:
            print(f"Socket error during receive: {e}")
            root.after(0, update_chat_box, f"--- Network error: {e} ---")
            break
        except Exception as e:
            print(f"Error receiving message: {e}")
            # Consider how to handle other errors, maybe break or continue
            break

def update_chat_box(message):
    """Safely updates the chat box from any thread."""
    try:
        chat_box.config(state='normal')
        chat_box.insert(tk.END, f"{message}\n")
        chat_box.yview(tk.END)
        chat_box.config(state='disabled')
    except tk.TclError:
        # Handle cases where the window might be closing
        print("Chat box update failed, window might be closing.")


def send_message(event=None): # Add event parameter for binding
    """Sends the message from the entry box."""
    msg = entry_box.get().strip() # Use strip()
    if msg:
        full_msg = f"{user_name}: {msg}"
        try:
            sock.sendto(full_msg.encode('utf-8'), (SERVER_IP, PORT)) # Specify encoding
            entry_box.delete(0, tk.END)
        except socket.error as e:
            print(f"Failed to send message: {e}")
            # Optionally inform the user via the chat box or a message box
            update_chat_box(f"--- Failed to send message: {e} ---")
        except Exception as e:
            print(f"Error sending message: {e}")
            update_chat_box(f"--- Error sending message: {e} ---")


# === UI Widgets Setup ===

# Chat Box
chat_box = scrolledtext.ScrolledText(
    root,
    state='disabled',
    wrap=tk.WORD,
    width=50,
    height=15,
    bg="#2c2c2c", # Consider using ttkbootstrap styles if possible
    fg="white",
    insertbackground="white",
    font=("Arial", 11)
)
chat_box.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

# Entry Box Frame (for better layout)
entry_frame = ttk.Frame(root)
entry_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

entry_box = ttk.Entry(
    entry_frame,
    # width=35, # Let expand handle width
    bootstyle="dark",
    font=("Arial", 11)
)
# Use grid or pack within the frame for better control
entry_box.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10)) # Add padding between entry and button
entry_box.bind("<Return>", send_message) # Pass the function directly
entry_box.focus_set() # Set focus after main window appears

# Send Button
# style = ttk.Style() # Style is usually managed by the theme
# style.configure("TButton", font=("Arial", 11)) # Font set by theme or widget option

send_button = ttk.Button(
    entry_frame,
    text="Send",
    command=send_message,
    # style="TButton", # Not needed if using bootstyle
    bootstyle="success"
)
send_button.pack(side=tk.LEFT)


# === Start Network Thread ===
recv_thread = threading.Thread(target=receive_messages, daemon=True)
recv_thread.start()

# === Initial Join Message ===
try:
    join_message = f"{user_name} has joined the chat."
    sock.sendto(join_message.encode('utf-8'), (SERVER_IP, PORT))
except socket.error as e:
    print(f"Failed to send join message: {e}")
    update_chat_box(f"--- Failed to announce join: {e} ---")


# === Run UI ===
root.mainloop()

# === Cleanup (optional, daemon thread usually handles exit) ===
print("Closing socket.")
sock.close()
