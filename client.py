import socket
import os

HOST = '127.0.0.1'
PORT = 5000

def upload_file(filename):
    if not os.path.exists(filename):
        print("File does not exist.")
        return

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

def list_files():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    client.sendall(b"LIST_FILES\n")
    response = client.recv(4096).decode()
    print("[File List]\n" + response.strip())
    client.close()

if __name__ == "__main__":
    while True:
        command = input("Enter command (UPLOAD <filename> / LIST_FILES / EXIT): ").strip()
        if command.startswith("UPLOAD "):
            _, fname = command.split(maxsplit=1)
            upload_file(fname)
        elif command == "LIST_FILES":
            list_files()
        elif command == "EXIT":
            print("Exiting client.")
            break
        else:
            print("Invalid command.")
