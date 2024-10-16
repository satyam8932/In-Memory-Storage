import time
from python.db import InMemoryDB

db = InMemoryDB()

# Set some keys
db.set('name', 'Satyam', 100000)
db.set('age', '30')

# Save the snapshot
db.save_snapshot('snapshot.json')

# Load the snapshot
db.load_snapshot('snapshot.json')

# Long-running loop to simulate a long-lived process
print("Database is running... Press Ctrl+C to stop.")
try:
    while True:
        # Simulate waiting for client requests (this could be extended to actually handle inputs)
        time.sleep(1)
except KeyboardInterrupt:
    # When the program is stopped (Ctrl+C), save a final snapshot before exiting
    print("\nSaving final snapshot before exiting...")
    db.save_snapshot('snapshot.json')
    print("Exiting.")
