# Python Socket Chat Room & Web Server 

## About the Project
This project is a lightweight, multi-client terminal chat application built entirely with Python's standard libraries. It features asynchronous, real-time messaging using socket programming and threading. Additionally, the repository includes a custom-built HTTP server designed to securely distribute the client script while blocking unauthorized directory access. 

It serves as a practical implementation of fundamental networking concepts, concurrent processing, and low-level server management in Python.

##  Technologies & Modules Used
* **Python 3**
* **`socket`:** Establishing TCP/IP connections for real-time data transfer.
* **`threading`:** Enabling concurrent execution to handle multiple clients and simultaneous send/receive operations seamlessly.
* **`http.server` & `socketserver`:** Creating a custom web server for local file distribution and controlled access.

## ✨ Key Features
* **Multi-Client Architecture:** The central server can handle multiple connections simultaneously, broadcasting messages to all active users.
* **Real-Time Asynchronous Chat:** Utilizing the `threading` module, users can receive incoming messages without being blocked by their own typing prompts.
* **Nickname Management:** A built-in system that assigns user handles and prevents duplicate nicknames from joining the room.
* **Custom HTTP File Server:** A dedicated web script (`web.py`) that serves the client file download natively while explicitly returning `403 Forbidden` errors for unauthorized directory listing attempts.

##   How to Run

### 1. Start the Chat Server
Run the main server script to open the chat room. By default, it listens on port `12345`.
```bash
python server.py