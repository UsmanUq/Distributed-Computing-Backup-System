import socket
import threading

# Keep track of connected storage nodes
storage_nodes = []

# Basic file metadata (filename -> list of nodes)
file_metadata = {}

HOST = '0.0.0.0'
PORT = 5000

def handle_client(conn, addr):
    print(f"[+] Connected by {addr}")
    try:
        data = conn.recv(1024).decode()
        if data.startswith("UPLOAD"):
            _, filename, filesize = data.strip().split()
            filesize = int(filesize)
            print(f"Receiving {filename} ({filesize} bytes)")
            
            file_content = b""
            while len(file_content) < filesize:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                file_content += chunk
            
            # Choose 2 storage nodes (for replication)
            if len(storage_nodes) < 2:
                print("[-] Not enough storage nodes connected!")
                conn.close()
                return
            
            selected_nodes = storage_nodes[:2]
            file_metadata[filename] = selected_nodes
            
            # Send file to storage nodes
            for node_conn in selected_nodes:
                try:
                    node_conn.sendall(f"STORE {filename} {filesize}\n".encode())
                    node_conn.sendall(file_content)
                    ack = node_conn.recv(1024).decode()
                    print(f"[Storage Node Reply] {ack.strip()}")
                except Exception as e:
                    print(f"Error sending to storage node: {e}")
            
            conn.sendall(b"UPLOAD_SUCCESS\n")
    
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        conn.close()

def handle_storage_node(conn, addr):
    print(f"[+] Storage Node connected from {addr}")
    storage_nodes.append(conn)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[Master Node] Listening on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        initial_data = conn.recv(1024).decode()
        if initial_data.startswith("STORAGE_NODE"):
            threading.Thread(target=handle_storage_node, args=(conn, addr)).start()
        else:
            threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start_server()
