---

# **Project Title: Distributed Backup System (Python)**

## **What is the Project?**
This project is a **simple distributed backup system** where a **master node** receives files from clients and **distributes** the file chunks across multiple **storage nodes**.  
The system ensures that uploaded files are **split**, **sent**, and **stored redundantly** across different nodes to improve **data reliability and availability**.

---

## **How the System Works**

### 1. **Components:**
- **Master Node**:
  - Acts as the central controller.
  - Accepts file uploads from clients.
  - Splits incoming files into smaller chunks.
  - Sends chunks to available storage nodes for saving.

- **Storage Nodes**:
  - Dedicated nodes that **store** file chunks sent by the master.
  - Communicate back with acknowledgments after successfully storing data.

- **Client**:
  - Connects to the master node to **upload** files.

---

### 2. **Workflow:**
- **Step 1**:  
  A client connects to the Master Node and sends an `UPLOAD` request along with the **filename** and **file size**.

- **Step 2**:  
  The Master Node **receives** the full file from the client.

- **Step 3**:  
  The file is **split into small chunks** (default chunk size = 1024 bytes).

- **Step 4**:  
  The Master selects two connected Storage Nodes to **distribute chunks** for **redundancy** (each node gets parts of the file).

- **Step 5**:  
  Each selected Storage Node receives and **stores** its assigned chunk.

- **Step 6**:  
  After storage is confirmed (acknowledgment received), the Master informs the Client that the **upload was successful**.

---

## **Technical Details**
- **Programming Language**: Python 3
- **Networking**: TCP sockets (`socket` module)
- **Multithreading**: Each client and storage node connection is handled on a **separate thread** for scalability.
- **Chunking**: Files are broken into **small pieces** to enable parallel storage and better fault tolerance.
- **Basic metadata tracking**: The Master keeps a record of which Storage Nodes store which file chunks.

---

## **Key Features**
- Basic **file redundancy** (stored in 2 nodes).
- **Parallel handling** of multiple clients and nodes using threads.
- **Error Handling**: Detects when insufficient storage nodes are available.
- **Easy Scalability**: More Storage Nodes can be added without changing Master Node logic.

---

#  **Summary**
This project demonstrates a **basic, scalable distributed backup system** architecture using Python. It mimics real-world distributed file systems by focusing on file chunking, storage node communication, redundancy, and fault tolerance.

---
