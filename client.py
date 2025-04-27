import socket
import os

HOST = '127.0.0.1'  # Master server IP
PORT = 5000

def upload_file(filename):
    filesize = os.path.getsize(filename)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    client.sendall(f"UPLOAD {filename} {filesize}\n".encode())
    
    with open(filename, "rb") as f:
        while True:
            bytes_read = f.read(4096)
            if not bytes_read:
                break
            client.sendall(bytes_read)
    
    response = client.recv(1024).decode()
    print("[Master Node Reply]", response.strip())

    client.close()

if __name__ == "__main__":
    fname = input("Enter filename to upload: ")
    upload_file(fname)
