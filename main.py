from flask import Flask, jsonify, request
from database import get_all_entries, get_entry, add_entry
from datetime import datetime, timezone
import os

app = Flask(__name__)


@app.route("/health")
def check():
    return "OK"


@app.route("/entries")
def list_entries():
    rows = get_all_entries()
    return jsonify([dict(r) for r in rows])


@app.route("/entries/<int:entry_id>")
def get_one(entry_id):
    row = get_entry(entry_id)
    if row is None:
        return jsonify({"error": "Entry not found"}), 404
    return jsonify(dict(row))


@app.route("/entries", methods=["POST"])
def create_entry():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Request body must be JSON"}), 400

    title = data.get("title")
    if not isinstance(title, str) or len(title) > 120:
        return jsonify({"error": "title is required, must be a string of max 120 characters"}), 400

    body = data.get("body")
    if not isinstance(body, str):
        return jsonify({"error": "body is required and must be a string"}), 400

    lat = data.get("lat")
    lon = data.get("lon")
    if lat is not None and not isinstance(lat, (int, float)):
        return jsonify({"error": "lat must be a number"}), 400
    if lon is not None and not isinstance(lon, (int, float)):
        return jsonify({"error": "lon must be a number"}), 400

    iso_time = datetime.now(timezone.utc).isoformat()
    new_id = add_entry(title, body, iso_time, lat, lon)
    row = get_entry(new_id)
    return jsonify(dict(row)), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
