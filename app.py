from flask import Flask, request, jsonify
import pymysql
import os

app = Flask(__name__)

# --- Database config (use environment variables in production) ---
DB_HOST = os.environ.get("DB_HOST", "<RDS-ENDPOINT>")
DB_USER = os.environ.get("DB_USER", "<your-username>")
DB_PASS = os.environ.get("DB_PASS", "<your-password>")
DB_NAME = os.environ.get("DB_NAME", "myapp")

def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route("/")
def home():
    return jsonify({"message": "Flask + MySQL RDS is working!"})

# CREATE
@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    title = data.get("title")
    if not title:
        return jsonify({"error": "title is required"}), 400

    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO tasks (title) VALUES (%s)", (title,))
        conn.commit()
        new_id = cursor.lastrowid
    conn.close()
    return jsonify({"id": new_id, "title": title, "done": False}), 201

# READ ALL
@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
    conn.close()
    return jsonify(tasks)

# READ ONE
@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
        task = cursor.fetchone()
    conn.close()
    if not task:
        return jsonify({"error": "not found"}), 404
    return jsonify(task)

# UPDATE
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()
    title = data.get("title")
    done = data.get("done")

    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute(
            "UPDATE tasks SET title = COALESCE(%s, title), done = COALESCE(%s, done) WHERE id = %s",
            (title, done, task_id)
        )
        conn.commit()
        affected = cursor.rowcount
    conn.close()
    if affected == 0:
        return jsonify({"error": "not found"}), 404
    return jsonify({"message": "updated"})

# DELETE
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        conn.commit()
        affected = cursor.rowcount
    conn.close()
    if affected == 0:
        return jsonify({"error": "not found"}), 404
    return jsonify({"message": "deleted"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
