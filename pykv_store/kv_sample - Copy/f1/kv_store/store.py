import threading
import time
import json
import os
from persistence import save_to_disk, write_wal
from recovery import load_from_disk

store = load_from_disk()
lock = threading.Lock()


# ---------------- PUT ----------------
def put_data(key, value, ttl=None):
    expiry = None
    if ttl:
        expiry = time.time() + int(ttl)

    old_value = store.get(key)

    store[key] = {
        "value": value,
        "expiry": expiry
    }

    write_wal("PUT", key, old_value, store[key])

    return {"message": "Saved successfully"}

# ---------------- GET ----------------
def get_data(key):
    data = store.get(key)

    if not data:
        return None

    if data["expiry"] and time.time() > data["expiry"]:
        del store[key]
        save_to_disk(store)
        return None

    return data["value"]


# ---------------- UPDATE ----------------
def update_data(key, value, ttl=None):
    with lock:
        if key not in store:
            return {"error": "Key not found"}

        old_value = store[key]

        expiry_time = store[key]["expiry"]
        if ttl:
            expiry_time = time.time() + int(ttl)

        store[key] = {
            "value": value,
            "expiry": expiry_time
        }

        write_wal("UPDATE", key, old_value, store[key])
        save_to_disk(store)

        return {"message": "Updated successfully"}


# ---------------- DELETE ----------------
def delete_data(key):
    with lock:
        if key not in store:
            return False

        old_value = store[key]
        del store[key]

        write_wal("DELETE", key, old_value, None)
        save_to_disk(store)

        return True


# ---------------- TTL CLEANER ----------------
def ttl_cleaner():
    while True:
        time.sleep(1)
        current_time = time.time()

        with lock:
            keys_to_delete = []

            for key, data in list(store.items()):
                if isinstance(data, dict):
                    expiry = data.get("expiry")

                    if expiry and current_time > expiry:
                        keys_to_delete.append(key)

            for key in keys_to_delete:
                del store[key]

            if keys_to_delete:
                save_to_disk(store)


# Start background cleaner thread
cleaner_thread = threading.Thread(target=ttl_cleaner, daemon=True)
cleaner_thread.start()