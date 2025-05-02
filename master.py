import socket
import threading

storage_nodes = []  # [(ip, port)]
file_metadata = {}  # filename -> list of (ip, port)

HOST = '0.0.0.0'
PORT = 5000

def handle_client(conn, addr, data):
    print(f"[+] Connected by client {addr}")
    try:
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

            if len(storage_nodes) < 2:
                print("[-] Not enough storage nodes connected!")
                conn.sendall(b"UPLOAD_FAILED: Not enough storage nodes\n")
                conn.close()
                return

            selected_nodes = storage_nodes[:2]
            file_metadata[filename] = selected_nodes

            for i, (node_ip, node_port) in enumerate(selected_nodes):
                try:
                    new_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    new_conn.connect((node_ip, node_port))
                    new_conn.sendall(f"STORE {filename} {len(file_content)}\n".encode())
                    new_conn.sendall(file_content)
                    ack = new_conn.recv(1024)
                    print(f"[+] Acknowledgment from node {i}: {ack.decode().strip()}")
                    new_conn.close()
                except Exception as e:
                    print(f"Error sending to storage node {i}: {e}")

            conn.sendall(b"UPLOAD_SUCCESS\n")

        elif data.strip() == "LIST_FILES":
            listing = ""
            for fname, nodes in file_metadata.items():
                node_list = ', '.join(f"{ip}:{port}" for ip, port in nodes)
                listing += f"{fname} => {node_list}\n"
            conn.sendall(listing.encode() if listing else b"No files available.\n")

    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        conn.close()

def handle_storage_node(conn, addr, port_data):
    try:
        if port_data.startswith("STORAGE_NODE"):
            _, port = port_data.strip().split()
            port = int(port)
            storage_nodes.append((addr[0], port))
            print(f"[+] Registered storage node at {addr[0]}:{port}")
        conn.close()
    except Exception as e:
        print(f"Error registering storage node: {e}")
        conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[Master Node] Listening on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        initial_data = conn.recv(1024).decode()
        if initial_data.startswith("STORAGE_NODE"):
            threading.Thread(target=handle_storage_node, args=(conn, addr, initial_data)).start()
        else:
            threading.Thread(target=handle_client, args=(conn, addr, initial_data)).start()

if __name__ == "__main__":
    start_server()
