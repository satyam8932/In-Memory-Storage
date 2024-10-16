
# In-Memory Database System

This document outlines the features of our custom in-memory database system, tools used, implementation steps, and additional features needed to build a system similar to Redis.

## Features Implemented

1. **In-Memory Key-Value Store**:
   - Stores key-value pairs in memory.
   - Supports setting, getting, and deleting keys.
   - Optionally sets a TTL (Time-to-Live) for key expiration.

2. **C++ Optimization**:
   - Critical operations (`set`, `get`, and `delete`) are optimized using C++ for better performance.
   - Exposed C++ functionality to Python using **Pybind11**.

3. **Multi-Threading** (Planned):
   - Support for multi-threaded operations to allow concurrent read/write operations.
   - Mutexes ensure thread safety for data operations.

4. **Snapshot-Based Persistence**:
   - Periodically saves the state of the database to disk in a JSON format (similar to Redis' RDB).
   - Captures both data and TTL values, allowing the database to restore its state after restarting.

5. **TTL (Time-to-Live) Support**:
   - Keys can have an expiration time, after which they are automatically deleted.
   - TTLs are stored as absolute timestamps for accurate expiration after system restarts.

## Tools and Libraries Used

1. **Python**:
   - Used for high-level functionality and testing of the database system.

2. **C++**:
   - Core performance-critical operations were implemented in C++ for efficiency.

3. **Pybind11**:
   - A Python binding library used to expose C++ functionality to Python.

4. **JSON (jsoncpp)**:
   - Used to handle snapshot saving and loading in JSON format.

5. **setuptools**:
   - Used to compile and link C++ code into a Python module.

6. **Mutex (std::mutex)**:
   - Used for thread safety in multi-threaded environments.

## Step-by-Step Implementation

### 1. Basic In-Memory Key-Value Store (Python)
- We first built the basic key-value store in Python with operations to `set`, `get`, and `delete` keys.
- TTL (Time-to-Live) was added for keys to expire after a specified time.

### 2. C++ Integration with Pybind11
- We optimized the core operations by moving them to C++.
- The `set`, `get`, and `delete` operations were implemented in C++.
- **Pybind11** was used to expose these C++ functions to Python, enabling seamless integration between Python and C++.

### 3. Multi-Threading Support (Planned)
- We planned to add multi-threading using C++ with `std::thread` and `std::mutex` for concurrent operations.
- Mutexes were introduced to ensure thread safety while performing read/write operations.

### 4. Snapshot-Based Persistence
- We implemented snapshot-based persistence similar to Redis' RDB (Redis Database Backup).
- This feature allows the database state (key-value pairs and TTLs) to be saved to disk in JSON format.
- The snapshot is loaded when the system restarts to restore the database state.
- TTLs are stored as absolute timestamps to ensure keys expire correctly after restoration.

### 5. Handling None for Expiration Time
- We handled `None` values for TTLs by defaulting to `0` (meaning no expiration) in Python when no TTL is specified.

### 6. Error Fixes (TypeError for None Expire Time)
- We fixed issues such as `TypeError` when passing `None` as the expiration time by ensuring proper defaults were passed to C++ functions.

## Missing Features to Build a Redis-Like System

To build a more complete Redis-like system, we would need to implement the following additional features:

1. **Append-Only File (AOF) Persistence**:
   - Implement an append-only log to capture write operations in real time.
   - This would allow the database to replay operations and recover with minimal data loss.

2. **Support for Advanced Data Types**:
   - Redis supports complex data structures like **lists**, **sets**, **sorted sets**, and **hashes**.
   - Adding these data structures would significantly expand the functionality of our system.

3. **Advanced Eviction Policies**:
   - Redis provides eviction policies such as **Least Recently Used (LRU)** and **Least Frequently Used (LFU)** to manage memory under pressure.
   - Implementing these policies would allow us to handle memory limits more efficiently.

4. **Replication and Clustering**:
   - Redis supports **replication** (master-slave architecture) for high availability and fault tolerance.
   - **Clustering** allows Redis to distribute data across multiple nodes, enabling horizontal scalability.

5. **Pub/Sub Messaging**:
   - Redis provides a **publish/subscribe** messaging model that allows clients to subscribe to channels and receive messages in real time.
   - Adding Pub/Sub would make our system more versatile for real-time applications.

6. **Lua Scripting**:
   - Redis allows users to run Lua scripts directly within the server.
   - Adding a scripting engine would enable users to perform complex operations atomically.

## Conclusion

While our in-memory database system includes essential features such as C++ optimization, multi-threading (planned), and snapshot persistence, there are several advanced features needed to make it comparable to Redis. These include AOF persistence, advanced data structures, eviction policies, and replication. By implementing these features, we can further improve the robustness, scalability, and versatility of our system.