from flask import Flask, jsonify
from database import get_all_entries, get_entry


app = Flask(__name__)
@app.route("/health")
def check():
	return "OK"

@app.route("/entries/<int:entry_id>")
def get_one(entry_id):
    row = get_entry(entry_id)
    if row is None:
        return jsonify({"error": "Entry not found"}), 404
    return jsonify(dict(row))
	
if __name__ == "__main__":
	app.run()
