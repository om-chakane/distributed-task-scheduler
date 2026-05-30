import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify, render_template_string
from broker.queue import TaskQueue

app = Flask(__name__)
queue = TaskQueue()

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Task Scheduler Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; background: #1e1e1e; color: #fff; padding: 40px; }
        h1 { color: #61dafb; }
        .stats { display: flex; gap: 20px; margin: 30px 0; }
        .card { background: #2d2d2d; border-radius: 10px; padding: 20px 40px; text-align: center; }
        .card h2 { font-size: 48px; margin: 10px 0; }
        .pending h2 { color: #f0c040; }
        .completed h2 { color: #4caf50; }
        .failed h2 { color: #f44336; }
        .card p { color: #aaa; font-size: 14px; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th { background: #2d2d2d; padding: 12px; text-align: left; color: #61dafb; }
        td { padding: 10px 12px; border-bottom: 1px solid #333; font-size: 13px; }
        tr:hover { background: #2d2d2d; }
        .status-completed { color: #4caf50; }
        .status-failed { color: #f44336; }
        .refresh { color: #aaa; font-size: 12px; margin-top: 10px; }
    </style>
    <meta http-equiv="refresh" content="3">
</head>
<body>
    <h1>Distributed Task Scheduler</h1>
    <p class="refresh">Auto-refreshes every 3 seconds</p>

    <div class="stats">
        <div class="card pending">
            <p>PENDING</p>
            <h2>{{ stats.pending }}</h2>
        </div>
        <div class="card completed">
            <p>COMPLETED</p>
            <h2>{{ stats.completed }}</h2>
        </div>
        <div class="card failed">
            <p>FAILED</p>
            <h2>{{ stats.failed }}</h2>
        </div>
    </div>

    <h2>Recent Completed Tasks</h2>
    <table>
        <tr>
            <th>Task ID</th>
            <th>Data</th>
            <th>Worker</th>
            <th>Attempts</th>
            <th>Status</th>
        </tr>
        {% for task in completed %}
        <tr>
            <td>{{ task.id[:8] }}...</td>
            <td>{{ task.data }}</td>
            <td>{{ task.get('worker_id', 'N/A') }}</td>
            <td>{{ task.attempts }}</td>
            <td class="status-completed">✓ completed</td>
        </tr>
        {% endfor %}
    </table>

    {% if failed %}
    <h2>Failed Tasks</h2>
    <table>
        <tr>
            <th>Task ID</th>
            <th>Data</th>
            <th>Attempts</th>
            <th>Error</th>
        </tr>
        {% for task in failed %}
        <tr>
            <td>{{ task.id[:8] }}...</td>
            <td>{{ task.data }}</td>
            <td>{{ task.attempts }}</td>
            <td class="status-failed">{{ task.get('error', 'unknown') }}</td>
        </tr>
        {% endfor %}
    </table>
    {% endif %}
</body>
</html>
"""

@app.route('/')
def dashboard():
    import json
    stats = queue.stats()
    
    completed_raw = queue.redis.lrange(queue.completed_key, 0, 20)
    completed = [json.loads(t) for t in completed_raw]
    
    failed_raw = queue.redis.lrange(queue.failed_key, 0, 20)
    failed = [json.loads(t) for t in failed_raw]
    
    return render_template_string(HTML, stats=stats, completed=completed, failed=failed)

@app.route('/api/stats')
def api_stats():
    return jsonify(queue.stats())

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5001)