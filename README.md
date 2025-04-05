# LocalChat
งานนี้เป็นส่วนหนึ่งของวิชา 968-230 Data Communications and Networking 2/2024
# LocalChat

**Project Overview**

LocalChat is a simple, local network chat application developed as part of the 968-230 Data Communications and Networking course (2/2024). It allows users on the same network to send and receive messages in real-time using UDP broadcast, without the need for an internet connection.

**Features**

*   **Local Network Communication:** Operates within a local network, enabling communication between devices connected to the same network via UDP broadcast.
*   **Real-time Messaging:** Messages are sent and received instantly.
*   **Simple Interface:** Easy-to-use command-line interface for the server and a graphical user interface (GUI) for the client.
*   **No Internet Required:** Functions entirely within the local network; no internet connection is needed.
*   **Username Support:** Users can choose a username upon connecting.
*   **Dynamic User Colors:** Each user is assigned a random color for visual distinction.
*   **GUI Client:** The client features a user-friendly graphical interface built with `tkinter` and `ttkbootstrap`.

**Getting Started**

**Prerequisites**

*   **Python 3.x:** Ensure you have Python 3 installed on your system. You can check by running `python --version` or `python3 --version` in your terminal.
*   **Sockets:** This project uses Python's built-in socket library, so no additional installation is required for this.
*   **Threading:** This project uses Python's built-in threading library, so no additional installation is required for this.
*   **ttkbootstrap:** The client uses the `ttkbootstrap` library for the GUI. Install it using:

    ```bash
    pip install ttkbootstrap
    ```

**Installation**

1.  **Clone the Repository (if applicable):** If the project is hosted on a version control system like Git, you can clone it using:

    ```bash
    git clone <repository_url>
    ```

2.  **Navigate to the Project Directory:**

    ```bash
    cd LocalChat
    ```

**How to Run**

1.  **Run the Server:**
    *   Open a terminal and navigate to the project directory.
    *   Run the server script:

    ```bash
    python server_BROADCAST_IP.py
    ```

    *   The server will start and listen for incoming connections on port `12345` using UDP broadcast.

2.  **Run the Client:**
    *   Open another terminal (or multiple terminals for multiple clients).
    *   Navigate to the project directory.
    *   Run the client script:

    ```bash
    python client_BROADCAST_IP.py
    ```

    *   The client will open a GUI window where you can enter your username and start chatting.

3.  **Start Chatting:**
    *   Once the client is connected, you can start sending messages.
    *   Type your message in the entry box and press Enter or click the "Send" button to send.
    *   Messages from other clients will appear in the chat box.

**How It Works**

*   **Server:**
    *   The server script (`server_BROADCAST_IP.py`) creates a UDP socket and binds it to the broadcast address (`255.255.255.255`) and port `12345`.
    *   It listens for incoming client connections and messages.
    *   When a client connects, the server assigns a random color to the user and stores their address and username.
    *   The server then broadcasts messages received from one client to all other connected clients.
    *   The server uses threading to handle multiple clients concurrently.
*   **Client:**
    *   The client script (`client_BROADCAST_IP.py`) creates a UDP socket and binds it to the same port `12345`.
    *   It uses `ttkbootstrap` to create a GUI for a user-friendly chat interface.
    *   It prompts the user to enter a username upon starting.
    *   It sends messages to the broadcast address, allowing all clients on the network to receive them.
    *   It also receives messages from the server and displays them in the chat box.
    *   The client uses threading to simultaneously send and receive messages.

**Project Structure**

*   `README.md`: This file, providing an overview and instructions for the project.
*   `server_BROADCAST_IP.py`: The Python script for running the chat server.
*   `client_BROADCAST_IP.py`: The Python script for running the chat client.

**Troubleshooting**

*   **Connection Issues:**
    *   Ensure that the server is running before starting the clients.
    *   Check that the server and clients are on the same local network.
    *   Firewall settings might be blocking the connection.
*   **Multiple Clients:**
    *   You can run multiple client instances to simulate a multi-user chat.
    *   Each client will need to connect to the server separately.

**Future Enhancements**

*   **Private Messaging:** Add the ability to send private messages to specific users.
*   **File Transfer:** Allow users to send files to each other.
*   **Encryption:** Implement encryption for secure communication.
*   **Improved GUI:** Enhance the GUI with more features and customization options.

**Contact**

If you have any questions or suggestions, feel free to reach out.
