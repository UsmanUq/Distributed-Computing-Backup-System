import socket
import threading
import os
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Storage Node")
    parser.add_argument('--port', type=int, required=True)
    return parser.parse_args()

HOST = '0.0.0.0'

def handle_client(conn, addr, storage_folder):
    print(f"[+] Connection from {addr}")

    header = b""
    while not header.endswith(b"\n"):
        header += conn.recv(1)
    header = header.decode().strip()
    print(f"[DEBUG] Header received: {header}")

    if header.startswith("STORE"):
        _, filename, filesize = header.strip().split()
        filesize = int(filesize)

        filepath = os.path.join(storage_folder, filename)
        with open(filepath, "wb") as f:
            received = 0
            while received < filesize:
                chunk = conn.recv(min(4096, filesize - received))
                if not chunk:
                    break
                f.write(chunk)
                received += len(chunk)

        conn.sendall(b"STORED\n")
        print(f"[+] Stored file: {filename} at {filepath}")
    else:
        print(f"[-] Unexpected command: {header}")

    conn.close()

def start_server(port):
    storage_folder = f"storage_data_node_{port}"
    os.makedirs(storage_folder, exist_ok=True)

    # Notify master
    try:
        master_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        master_conn.connect(('127.0.0.1', 5000))
        master_conn.sendall(f"STORAGE_NODE {port}\n".encode())
        master_conn.close()
    except Exception as e:
        print(f"[!] Could not register with master: {e}")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, port))
    server_socket.listen(5)
    print(f"[+] Storage Node listening on {HOST}:{port}")

    while True:
        conn, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(conn, addr, storage_folder)).start()

def command_listener(port):
    folder = f"storage_data_node_{port}"
    while True:
        cmd = input()
        if cmd.strip().lower() == "status":
            files = os.listdir(folder)
            print("Files stored:", files)

if __name__ == "__main__":
    args = parse_args()
    threading.Thread(target=command_listener, args=(args.port,), daemon=True).start()
    start_server(args.port)
