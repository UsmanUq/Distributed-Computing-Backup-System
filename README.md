# Distributed File Storage System (Master + Storage Nodes + Client)

## 📌 Overview

This is a basic distributed file storage system built with Python's `socket` and `threading` libraries. It consists of:

- A **Master Node** that coordinates storage and metadata.
- Multiple **Storage Nodes** that store files.
- A **Client** that can upload files and list available files.

---

## 🧠 Architecture

```
     [Client] ---> [Master Node] ---> [Storage Node 1]
                   |              ---> [Storage Node 2]
                   |              ---> [Storage Node 3]
                   ...
```

- The **Client** connects to the Master Node to upload a file or list available files.
- The **Master Node** stores metadata and sends file data to two connected storage nodes.
- **Storage Nodes** register themselves with the Master and store file data sent by the Master.

---

## ✅ Current Features

### 1. Upload File
- Client sends: `UPLOAD filename filesize`
- Master receives the file and stores it on **two available storage nodes**.
- Master updates metadata with storage locations for future retrieval.
- Acknowledgment is sent back to the client.

### 2. Register Storage Nodes
- A storage node sends: `STORAGE_NODE port`
- Master registers the node using the sender’s IP and given port.
- The node is now eligible to receive files from the Master.

### 3. List Files (Client)
- Client sends: `LIST`
- Master returns all uploaded filenames with the IP/Port of the storage nodes where each file is stored.

---

## 🗃 Metadata Structure (in Master)

```python
file_metadata = {
    'example.txt': [
        ('192.168.1.5', 5001),
        ('192.168.1.6', 5002)
    ]
}
```

---

## 🖥 Terminal Workflow

### 🔸 Start Storage Nodes

```bash
python storage_node.py 5001
python storage_node.py 5002
python storage_node.py 5003
```

Each storage node registers with the master on launch.

### 🔹 Start Master Node

```bash
python master_node.py
```

The master listens for storage nodes and clients on port 5000.

### 🔸 Start Client

```bash
python client.py
```

You can now:
- Upload a file (`upload filename.txt`)
- List available files (`list`)
- Exit the client (`exit`)

> The client terminal remains active to accept multiple commands without restarting.

---

## 🚧 To-Do (Planned)

- [ ] Add **file chunking** (split file into parts).
- [ ] Store each chunk **redundantly** across multiple nodes.
- [ ] Add **file download** and **recovery** from chunks.
- [ ] Use **hashes** to verify chunk integrity.
- [ ] Auto-repair chunks on node failure.

---

## 📁 Folder Structure

```
distributed_storage/
│
├── master_node.py        # Coordinates storage and metadata
├── storage_node.py       # Stores uploaded files
├── client.py             # Uploads and lists files
├── README.md             # You are here
```

---

## 🧑‍💻 Author

Developed by [UsmanUq] as part of a distributed systems learning project.

---

Let me know if you’d like a logo, project badge, or repo description snippet!
