import json
import os
import time

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

STORE_FILE = os.path.join(DATA_DIR, "store.json")
WAL_FILE = os.path.join(DATA_DIR, "wal.log")


def write_wal(operation, key, old_value=None, new_value=None):
    os.makedirs("data", exist_ok=True)

    log_entry = {
        "operation": operation,
        "key": key,
        "old_value": old_value,
        "new_value": new_value,
        "timestamp": time.time()
    }

    with open("data/wal.log", "a") as f:
        f.write(json.dumps(log_entry) + "\n")

def save_to_disk(store):
    with open(STORE_FILE, "w") as f:
        json.dump(store, f, indent=4)