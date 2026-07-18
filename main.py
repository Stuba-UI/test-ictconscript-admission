from flask import Flask, jsonify
from database import get_all_entries


app = Flask(__name__)
@app.route("/health")
def check():
	return "OK"

@app.route("/entries")
def list_entries():
    rows = get_all_entries()
    return jsonify([dict(r) for r in rows])
	
if __name__ == "__main__":
	app.run()
