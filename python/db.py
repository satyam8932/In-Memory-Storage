import time
import sys
import os
import json

# Add the build folder to the Python path
sys.path.append(os.path.abspath('build/lib.linux-x86_64-cpython-311'))

# Try importing the C++ module
try:
    import database
    print("Using C++ module")
except ImportError:
    # Fall back to the Python version if C++ is not available
    print("Using Python fallback.")
    database = None

class InMemoryDB:
    def __init__(self):
        if database:
            # If C++ module is available, use it
            self.db = database.InMemoryDB()
        else:
            # Fallback to Python implementation
            self.data = {}
            self.ttl = {}

    def set(self, key: str, value: any, expire_in_seconds: int = None):
        if database:
            expire_in_seconds = expire_in_seconds or 0  # None is not a valid thing in C++
            self.db.set(key, value, expire_in_seconds)
        else:
            self.data[key] = value
            if expire_in_seconds:
                self.ttl[key] = time.time() + expire_in_seconds

    def get(self, key: str):
        if database:
            return self.db.get(key)
        else:
            if key in self.ttl and time.time() > self.ttl[key]:
                del self.data[key]
                del self.ttl[key]
                return None
            return self.data.get(key)

    def delete(self, key: str):
        if database:
            return self.db.delete(key)
        else:
            if key in self.data:
                del self.data[key]
                if key in self.ttl:
                    del self.ttl[key]
                return True
            return False

    def clean_expired(self):
        if not database:
            current_time = time.time()
            keys_to_delete = [key for key, expire_at in self.ttl.items() if current_time > expire_at]
            for key in keys_to_delete:
                self.delete(key)
    
    def save_snapshot(self, filename='snapshot.json'):
        if database:
            self.db.save_snapshot(filename)
        else:
            with open(filename, 'w') as f:
                snapshot = {
                    'data': self.data,
                    'ttl': {key: self.ttl[key] for key in self.ttl}
                }
                json.dump(snapshot, f)
        print(f"Snapshot saved to {filename}")

    def load_snapshot(self, filename='snapshot.json'):
        if database:
            self.db.load_snapshot(filename)
        else:
            try:
                with open(filename, 'r') as f:
                    snapshot = json.load(f)
                    self.data = snapshot['data']
                    current_time = time.time()
                    self.ttl = {key: ttl for key, ttl in snapshot['ttl'].items() if ttl > current_time}
            except FileNotFoundError:
                print(f"No snapshot file found: {filename}")
        print(f"Snapshot loaded from {filename}")
