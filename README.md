# OPC-UA Playground 🏗️  
*A lightweight OPC UA Server & Client implementation in Python for learning, testing and integration with Digital Twin systems.*

---

## 📖 Overview

**OPC UA (Open Platform Communications – Unified Architecture)** is an open, cross-platform communication protocol designed for secure and reliable exchange of industrial data.  
It’s widely used in **Industry 4.0**, **Digital Twins**, and **Industrial IoT** applications to enable interoperability between devices, controllers, and software from different vendors.

This repository provides a **minimal yet extensible** example of an OPC UA **Server–Client** system built with Python, focusing on:
- clarity and simplicity for educational purposes;
- modularity for future extensions (e.g., MQTT bridge, REST APIs, etc.);
- structured OOP design suitable for integration in larger automation systems.

---

## ⚙️ Features

✅ **Python-based OPC UA Server** that exposes simulated industrial devices  
✅ **Client** capable of browsing, reading, and live-monitoring variables  
✅ **Real-time data update loop** (temperature, pressure, etc.)  
✅ **Object-oriented structure**, easy to expand with new devices  
✅ **Error handling and robustness** (skips invalid nodes gracefully)  
✅ Compatible with any OPC UA client (e.g. *UaExpert*, *Prosys*, *Node-RED*, *Ignition*)

---

## 🧩 Repository Structure

```text
📦 opc-ua-playground/
│
├── [server.py](./server.py) # OPC UA server: creates and updates devices & variables
├── [client.py](./client.py) # OPC UA client: connects, browses, and monitors variables
├── [requirements.txt](./requirements.txt) # Dependencies
└── [README.md](./README.md) # This file
```

---

## 🚀 Getting Started

### 1️⃣ Prerequisites

#### 1. Clone the repository
```bash
git clone https://github.com/davide-z99/opc-ua-playground.git
cd opc-ua-playground
```
#### 2. Install the dependencies

```bash
pip install -r requirements.txt
```

⚠️ If you see the message:
```csharp
cryptography is not installed, use of crypto disabled
```
You can fix it by manually installing:
```bash
pip install cryptography
```

### 2️⃣ Run the Server

```bash
python server.py
```

You should see:
```bash
OPC UA Server started at opc.tcp://localhost:4840/freeopcua/server/
```

The server will periodically update the device variables.

### 3️⃣ Run the Client
In another terminal:
```bash
python client.py
```
Expected output example:
```bash
Connected to OPC UA Server at opc.tcp://localhost:4840/freeopcua/server/

Found device: Thermometer_1
 - Temperature: 20.1
 - Pressure: 1.03
 - Running: True

Found device: Barometer_2
 - Temperature: 20.4
 - Pressure: 1.02
 - Running: False
```
The client will:
- Connect to the server
- Browse all devices and variables
- Print live data updates in real time

You can stop monitoring anytime with **Ctrl+C**


## 🧠 A Quick Refresher on OPC UA
### 🔹 What is OPC UA?

OPC UA stands for Open Platform Communications – Unified Architecture.
It’s the evolution of the classic OPC protocol, re-designed to be:
- Platform-independent (runs on Windows, Linux, embedded, etc.)
- Service-oriented (based on an address space with - nodes and attributes)
- Secure by design (supports encryption, authentication, and authorization)
- Scalable (from small devices to cloud systems)

---

### 🔹 Core Concepts
| Concept           | Description                                                                               |
| ----------------- | ----------------------------------------------------------------------------------------- |
| **Server**        | Hosts data and exposes it as objects and variables.                                       |
| **Client**        | Connects to the server, reads/writes variables, subscribes to changes.                    |
| **Namespace**     | A unique identifier space to avoid naming collisions between vendors.                     |
| **Node**          | The basic element in the OPC UA address space (can be an Object, Variable, Method, etc.). |
| **Attributes**    | Properties of nodes (e.g., *Value*, *DisplayName*, *NodeId*).                             |
| **Subscriptions** | Mechanism for clients to get notified when a value changes.                               |

---

### 🔹 How It Works (Simplified)

1. The Server defines an address space with a hierarchy of nodes (objects, variables, methods).
2. The Client connects via TCP (opc.tcp://...) and requests access to specific nodes.
3. The client can:
    - Browse the structure (discover available nodes)
    - Read or write variable values
    - Subscribe to updates (receive push notifications)
---
### 🧱 Common Obstacles & Debugging Notes
| Problem                            | Cause                                      | Solution                                                                     |
| ---------------------------------- | ------------------------------------------ | ---------------------------------------------------------------------------- |
| ❌ `TimeoutError: timed out`        | No OPC UA server running                   | Start `server.py` before the client                                          |
| ⚠️ `BadNoMatch`                    | Wrong node path (namespace/index mismatch) | Check namespace indexes using `get_browse_name()` or `get_namespace_array()` |
| ⚠️ `BadAttributeIdInvalid`         | Trying to read a non-variable node         | Check node class with `get_node_class()` before calling `get_value()`        |
| ⚠️ `cryptography is not installed` | Optional package missing                   | Install with `pip install cryptography`                                      |
| ⚠️ Server stops updating           | Main loop blocked                          | Use non-blocking or threaded updates for future scalability                  |

## 🧩 Extending the Project

Future enhancements could include:
- [] MQTT bridge (bidirectional OPC UA ⇄ MQTT data exchange)
- [] Web dashboard for real-time visualization
- [] Logging historical data to a database (e.g., InfluxDB)
- [] Integration with Digital Twin frameworks
- [] Deployment in Docker containers

## 👨‍💻 Author
<div style="display: flex; flex-direction: column; gap: 25px;">
    <!-- Davide Ziglioli -->
    <div style="display: flex; align-items: center; gap: 15px;">
        <img src="ziglioli.jpg" width="60" style="border-radius: 50%; border: 2px solid #eee;"/>
        <div>
        <h3 style="margin: 0;">Davide Ziglioli</h3>
        <p style="margin: 4px 0;">Digital Automation Engineering Graduated Student<br> University of Modena and Reggio Emilia, Department of Sciences and Methods for Engineering (DISMI)</p>
        <div>
            <a href="https://www.linkedin.com/in/davide-ziglioli/">
            <img src="https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat-square&logo=linkedin"/>
            </a>
            <a href="https://github.com/davide-z99" style="margin-left: 8px;">
            <img src="https://img.shields.io/badge/GitHub-Profile-black?style=flat-square&logo=github"/>
            </a>
        </div>
        </div>
    </div>

## 🧭 References
- [OPC Foundation Official Site](https://opcfoundation.org/)
- [FreeOpcUa Python Library Docs](https://github.com/FreeOpcUa/python-opcua)
- [Unified Architecture Specification](https://reference.opcfoundation.org)