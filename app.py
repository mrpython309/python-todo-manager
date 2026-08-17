"""
Smart Task Manager Web Application
Author: Anees Shaikh
Description: Lightweight Python HTTP REST server & Web Interface with zero external dependencies.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import urllib.parse
import webbrowser
from datetime import datetime

STORAGE_FILE = "tasks.json"

def load_data():
    if os.path.exists(STORAGE_FILE):
        try:
            with open(STORAGE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"next_id": 1, "tasks": []}

def save_data(data):
    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Task Manager — Python 3</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; }
        body { background: #0f172a; color: #f8fafc; display: flex; justify-content: center; padding: 40px 20px; }
        .container { width: 100%; max-width: 800px; background: #1e293b; border-radius: 12px; padding: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.4); }
        .header { text-align: center; border-bottom: 2px solid #334155; padding-bottom: 16px; margin-bottom: 20px; }
        .header h1 { font-size: 24px; font-weight: 700; color: #38bdf8; }
        .header p { font-size: 13px; color: #94a3b8; margin-top: 4px; }
        .form-card { background: #0f172a; padding: 16px; border-radius: 8px; margin-bottom: 20px; display: grid; grid-template-columns: 2fr 1fr 1fr auto; gap: 10px; align-items: center; }
        input, select { background: #1e293b; border: 1px solid #475569; color: #fff; padding: 10px 12px; border-radius: 6px; font-size: 13px; outline: none; }
        input:focus, select:focus { border-color: #38bdf8; }
        .btn-add { background: #0284c7; color: white; border: none; padding: 10px 18px; border-radius: 6px; font-weight: 600; cursor: pointer; transition: 0.2s; }
        .btn-add:hover { background: #0369a1; }
        .task-list { display: flex; flex-direction: column; gap: 10px; }
        .task-item { background: #0f172a; border: 1px solid #334155; border-radius: 8px; padding: 14px; display: flex; justify-content: space-between; align-items: center; }
        .task-item.completed { opacity: 0.6; text-decoration: line-through; }
        .task-info h4 { font-size: 15px; color: #f1f5f9; }
        .badges { display: flex; gap: 8px; margin-top: 6px; }
        .badge { font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 4px; }
        .badge-work { background: #1e3a8a; color: #93c5fd; }
        .badge-personal { background: #831843; color: #fbcfe8; }
        .badge-high { background: #7f1d1d; color: #fca5a5; }
        .badge-med { background: #78350f; color: #fde68a; }
        .actions { display: flex; gap: 8px; }
        .btn-done { background: #16a34a; color: white; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; font-size: 12px; font-weight: 600; }
        .btn-del { background: #dc2626; color: white; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; font-size: 12px; font-weight: 600; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📋 Smart Task Manager & To-Do App</h1>
            <p>Python 3 REST API Backend & Modern Responsive UI</p>
        </div>
        
        <form class="form-card" id="taskForm">
            <input type="text" id="title" placeholder="Task Title..." required>
            <select id="category">
                <option value="General">General</option>
                <option value="Work">Work</option>
                <option value="Personal">Personal</option>
                <option value="Study">Study</option>
            </select>
            <select id="priority">
                <option value="High">High Priority</option>
                <option value="Medium" selected>Medium Priority</option>
                <option value="Low">Low Priority</option>
            </select>
            <button type="submit" class="btn-add">+ Add Task</button>
        </form>

        <div class="task-list" id="taskList"></div>
    </div>

    <script>
        async function fetchTasks() {
            const res = await fetch('/api/tasks');
            const data = await res.json();
            const list = document.getElementById('taskList');
            list.innerHTML = '';

            if (data.tasks.length === 0) {
                list.innerHTML = '<p style="text-align:center; color:#64748b; padding:20px;">No tasks found. Add a task above!</p>';
                return;
            }

            data.tasks.forEach(t => {
                const div = document.createElement('div');
                div.className = `task-item ${t.completed ? 'completed' : ''}`;
                div.innerHTML = `
                    <div class="task-info">
                        <h4>#${t.task_id} ${t.title}</h4>
                        <div class="badges">
                            <span class="badge badge-${t.category.toLowerCase()}">${t.category}</span>
                            <span class="badge badge-${t.priority.toLowerCase() === 'high' ? 'high' : 'med'}">${t.priority}</span>
                            <span class="badge" style="background:#334155; color:#94a3b8">${t.created_at}</span>
                        </div>
                    </div>
                    <div class="actions">
                        ${!t.completed ? `<button class="btn-done" onclick="completeTask(${t.task_id})">✓ Complete</button>` : ''}
                        <button class="btn-del" onclick="deleteTask(${t.task_id})">🗑 Delete</button>
                    </div>
                `;
                list.appendChild(div);
            });
        }

        document.getElementById('taskForm').onsubmit = async (e) => {
            e.preventDefault();
            const title = document.getElementById('title').value;
            const category = document.getElementById('category').value;
            const priority = document.getElementById('priority').value;

            await fetch('/api/tasks', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({title, category, priority})
            });

            document.getElementById('title').value = '';
            fetchTasks();
        };

        async function completeTask(id) {
            await fetch(`/api/tasks/complete?id=${id}`, {method: 'POST'});
            fetchTasks();
        }

        async function deleteTask(id) {
            await fetch(`/api/tasks/delete?id=${id}`, {method: 'POST'});
            fetchTasks();
        }

        fetchTasks();
    </script>
</body>
</html>
"""

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode("utf-8"))
        elif self.path == "/api/tasks":
            data = load_data()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        data = load_data()
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length > 0 else b'{}'
        
        if self.path == "/api/tasks":
            payload = json.loads(body.decode("utf-8"))
            new_task = {
                "task_id": data["next_id"],
                "title": payload.get("title", "").strip(),
                "category": payload.get("category", "General"),
                "priority": payload.get("priority", "Medium"),
                "completed": False,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            data["tasks"].append(new_task)
            data["next_id"] += 1
            save_data(data)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode("utf-8"))

        elif self.path.startswith("/api/tasks/complete"):
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            task_id = int(params.get("id", [0])[0])
            for t in data["tasks"]:
                if t["task_id"] == task_id:
                    t["completed"] = True
                    break
            save_data(data)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode("utf-8"))

        elif self.path.startswith("/api/tasks/delete"):
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            task_id = int(params.get("id", [0])[0])
            data["tasks"] = [t for t in data["tasks"] if t["task_id"] != task_id]
            save_data(data)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode("utf-8"))

def run():
    port = 5000
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)
    url = f"http://localhost:{port}"
    print(f"✓ Smart Task Manager server running at {url}")
    webbrowser.open(url)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")

if __name__ == "__main__":
    run()
