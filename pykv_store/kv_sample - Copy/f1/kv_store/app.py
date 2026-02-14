from flask import Flask, request, jsonify, render_template
from store import(
    put_data,
    get_data,
    delete_data,
    update_data,
   
)

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("dashboard.html")
    
@app.route("/store")
def store():
    return render_template("index.html")
    
# PUT
@app.route("/put", methods=["PUT"])
def put():
    key = request.args.get("key")
    value = request.args.get("value")
    ttl = request.args.get("ttl")

    if not key or not value:
        return jsonify({"error": "Key and value required"}), 400

    ttl = int(ttl) if ttl else None

    return jsonify(put_data(key, value, ttl))
# GET
@app.route("/get", methods=["GET"])
def get():
    key = request.args.get("key")

    if not key:
        return jsonify({"error": "Key required"}), 400

    value = get_data(key)

    if value is None:
        return jsonify({"error": "Key not found"}), 404

    return jsonify({"key": key, "value": value})


# UPDATE
@app.route("/update", methods=["PUT"])
def update():
    key = request.args.get("key")
    value = request.args.get("value")
    

    if not key or not value:
        return jsonify({"error": "Key and value required"}), 400
   

    return jsonify(update_data(key,value))

# DELETE
@app.route("/delete", methods=["DELETE"])
def delete():
    key = request.args.get("key")

    if not key:
        return jsonify({"error": "Key required"}), 400

    success = delete_data(key)

    if not success:
        return jsonify({"error": "Key not found"}), 404

    return jsonify({"message": "Deleted successfully"})




@app.route("/ttl", methods=["GET"])
def ttl():
    key = request.args.get("key")

    if not key:
        return jsonify({"error": "Key required"}), 400

    from store import store
    import time

    if key not in store:
        return jsonify({"error": "Key not found"}), 404

    expiry = store[key]["expiry"]

    if not expiry:
        return jsonify({"message": "No TTL set"})

    remaining = int(expiry - time.time())

    if remaining <= 0:
        return jsonify({"error": "Key expired"}), 404

    return jsonify({"ttl_remaining": remaining})

@app.route("/keys", methods=["GET"])
def keys():
    from store import store
    return jsonify({"keys": list(store.keys())})

@app.route("/logs", methods=["GET"])
def logs():
    import os
    import json

    if not os.path.exists("data/wal.log"):
        return jsonify({"logs": []})

    with open("data/wal.log", "r") as f:
        lines = f.readlines()

    entries = [json.loads(line) for line in lines]

    return jsonify({"logs": entries})


if __name__ == "__main__":
    app.run(debug=False)