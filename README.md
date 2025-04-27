# Distributed-Computing-Backup-System

- **Server = Master Node** (small server running with `socketserver` or manual `socket` handling)
- **Clients = Storage Nodes + User Client** (simple Python scripts that connect and send/receive files)
- **Metadata = Simple dictionary in memory** (no DB needed, or use SQLite if you want to be fancy)

---

# 📜 Very Simple Plan

### Architecture
```
[User Client] 
    ↓ (uploads file via socket)
[Master Node] 
    ↙︎           ↘︎
[Storage Node 1]  [Storage Node 2]
```
- **User client** connects to **master** and sends a file.
- **Master** decides which **Storage Nodes** to send the file to.
- **Master** keeps a small in-memory mapping like:
  ```python
  metadata = {
    "my_resume.pdf": ["Node1", "Node2"]
  }
  ```
- **Replication**: Send same file to 2 or 3 storage nodes.

---

# 🛠️ Technologies
- **Python 3.x**
- `socket` module
- maybe `threading` for handling multiple connections
- VSCode with `.ipynb` is okay too (but sockets work better in `.py` files if needed)

---

# 🚀 Example Mini Architecture (Simple Socket Flow)

### 1. **Master Node (Server)**
- Listens for connections from **clients** (User Client, Storage Nodes)
- Handles simple commands like:
  - `"STORE filename filesize"`
  - `"RETRIEVE filename"`
  - `"NODE_HEARTBEAT"`

### 2. **Storage Node (Server)**
- Listens for file uploads from **Master**.
- Stores files locally (in a `storage/` folder).

### 3. **Client (Uploader)**
- Connects to **Master**.
- Asks to store a file (uploads file).

---

# 📦 Minimum Features You Can Implement

| Feature | How | 
|:--------|:----|
| File Upload | User Client → Master → Storage Nodes |
| Replication | Master picks 2-3 Storage Nodes |
| Metadata Management | Master stores mapping in Python dictionary |
| Fault tolerance (basic) | Detect if a Storage Node is offline |
---
