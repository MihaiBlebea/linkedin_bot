from flask import Flask, jsonify
import os

import sqlite3

app = Flask(__name__)

conn = sqlite3.connect("store.db", check_same_thread=False)
cursor = conn.cursor()

@app.route('/')
@app.route('/updates')
def updates():
	cursor = conn.cursor()
	rows = cursor.execute("SELECT * FROM jobs").fetchall()

	result = []
	for r in rows:
		result.append({
			"id": r[0],
			"title": r[1],
			"url": r[2],
			"unique_id": r[3],
			"salary_low": r[4],
			"salary_high": r[5],
			"created": r[6]
		})

	return jsonify(result)


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=int(os.environ.get("HTTP_PORT", 5000)))