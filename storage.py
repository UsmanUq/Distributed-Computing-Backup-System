import socket
import threading
import os
import argparse

# Parse command-line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Storage Node")
    parser.add_argument('--port', type=int, required=True, help="Port number for the storage node")
    return parser.parse_args()

# Settings
HOST = '0.0.0.0'  # Listen on all interfaces

# Storage folder
STORAGE_FOLDER = 'storage_data'

# Create storage folder if it doesn't exist
if not os.path.exists(STORAGE_FOLDER):
    os.makedirs(STORAGE_FOLDER)

# Handle client connection
def handle_client(conn, addr):
    print(f"[+] Connection from {addr}")

    try:
        # Receive filename
        filename = conn.recv(1024).decode()
        if not filename:
            print("[-] No filename received")
            return
        
        filepath = os.path.join(STORAGE_FOLDER, filename)
        
        # Receive file data
        with open(filepath, 'wb') as f:
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                f.write(data)

        print(f"[+] Stored file: {filename}")
    except Exception as e:
        print(f"[-] Error: {e}")
    finally:
        conn.close()

# Start the server
def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, port))
    server_socket.listen(5)
    print(f"[+] Storage Node listening on {HOST}:{port}")

    while True:
        conn, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr)).start()
        client_thread.start()

# Main function
if __name__ == "__main__":
    args = parse_args()
    start_server(args.port)

def command_listener():
    while True:
        cmd = input()
        if cmd.strip().lower() == "status":
            files = os.listdir('storage_data')
            print("Files stored:", files)

threading.Thread(target=command_listener, daemon=True).start()

