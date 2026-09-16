"""
Simple Task Tracker web application.
Built for CSI2113 Practical Assessment — Containerized Web Application with CI/CD.
"""
from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime

app = Flask(__name__)

# In-memory task store (fine for a demo app; resets on restart)
tasks = []
next_id = 1


@app.route("/")
def index():
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add_task():
    global next_id
    title = request.form.get("title", "").strip()
    if title:
        tasks.append({
            "id": next_id,
            "title": title,
            "done": False,
            "created": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        })
        next_id += 1
    return redirect(url_for("index"))


@app.route("/complete/<int:task_id>", methods=["POST"])
def complete_task(task_id):
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = not t["done"]
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return redirect(url_for("index"))


@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "task_count": len(tasks)}), 200


@app.route("/api/tasks")
def api_tasks():
    return jsonify(tasks), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
