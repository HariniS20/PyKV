import json
import os

STORE_FILE = "data/store.json"
WAL_FILE = "data/wal.log"



def load_from_disk():
    store = {}

    if not os.path.exists("data/wal.log"):
        return store

    with open("data/wal.log", "r") as f:
        lines = f.readlines()

    for line in lines:
        entry = json.loads(line)

        op = entry.get("operation")
        key = entry.get("key")

        if op == "PUT" or op == "UPDATE":
            store[key] = entry.get("new_value")

        elif op == "DELETE":
            if key in store:
                del store[key]

    return store