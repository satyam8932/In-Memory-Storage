
In-Memory Database System Development

## What We've Done So Far:
1. **In-Memory Key-Value Store**: 
   - Built a basic key-value store in Python that supports `set`, `get`, and `delete` operations.
   - Implemented TTL (Time-to-Live) for keys to expire after a set time.

2. **C++ Optimization**:
   - Moved critical operations (like `set`, `get`, and `delete`) to C++ for performance.
   - Used Pybind11 to expose the C++ functions to Python.

3. **Snapshot-Based Persistence**:
   - Added snapshot functionality, saving the state of the in-memory database to disk.
   - Implemented a method to load snapshots on program startup.

4. **Tested Basic Socket Server** (Explored but decided to switch):
   - Implemented a basic TCP server that could handle requests to store and retrieve data, but decided to shift to a web-based approach.

5. **Planned Transition to Web Server with FastAPI**:
   - Decided to move forward by setting up a FastAPI web server, which will act as the backend for the in-memory database.
   - FastAPI will handle HTTP requests for storing, retrieving, and deleting data using the in-memory database system.

## Future Tasks:
1. **Set Up FastAPI Web Server**:
   - Create a FastAPI web server to handle HTTP requests (GET, POST, DELETE).
   - Integrate the existing in-memory database code into the FastAPI routes.

2. **Implement API Endpoints**:
   - `POST /set`: Store key-value pairs with optional TTL.
   - `GET /get`: Retrieve the value of a key.
   - `DELETE /delete`: Delete a key from the database.

3. **Persistence**:
   - Continue to use snapshot-based persistence to save the state of the database on server shutdown.
   - Load snapshots automatically when the server starts.

4. **Extend the System** (Optional, future considerations):
   - Explore real-time persistence (Append-Only File - AOF).
   - Handle advanced features like replication, clustering, or more complex data types (e.g., lists, sets).

This summary covers what we've achieved so far and outlines the next steps. The primary focus will be setting up the FastAPI server and integrating the in-memory database system into a web-based architecture.
