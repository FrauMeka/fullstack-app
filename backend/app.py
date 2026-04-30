from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import time
import psycopg2

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.getenv("DATABASE_URL")


def get_conn():
    for i in range(10):
        try:
            return psycopg2.connect(DATABASE_URL)
        except psycopg2.OperationalError:
            print("Waiting for PostgreSQL...")
            time.sleep(3)

    raise Exception("PostgreSQL is not ready")


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            student_id TEXT NOT NULL
        )
    """)

    conn.commit()
    cur.close()
    conn.close()


@app.route("/")
def home():
    return "Backend is running"


@app.route("/api/data", methods=["GET"])
def get_data():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT id, name, student_id FROM students ORDER BY id")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    data = []

    for row in rows:
        data.append({
            "id": row[0],
            "name": row[1],
            "student_id": row[2]
        })

    return jsonify(data)


@app.route("/api/data", methods=["POST"])
def add_data():
    data = request.json

    name = data.get("name")
    student_id = data.get("student_id")

    if not name or not student_id:
        return jsonify({"error": "name and student_id are required"}), 400

    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO students (name, student_id) VALUES (%s, %s) RETURNING id",
        (name, student_id)
    )

    new_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        "id": new_id,
        "name": name,
        "student_id": student_id
    }), 201


@app.route("/api/data/<int:item_id>", methods=["DELETE"])
def delete_data(item_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("DELETE FROM students WHERE id = %s", (item_id,))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Deleted successfully"})


if __name__ == "__main__":
    init_db()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
