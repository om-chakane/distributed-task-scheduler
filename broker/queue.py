import redis
import json
import uuid
from datetime import datetime

class TaskQueue:
    def __init__(self, host=None, port=6379):
        import os
        host = host or os.environ.get('REDIS_HOST', 'localhost')
        self.redis = redis.Redis(host=host, port=port, decode_responses=True)
        self.queue_key = "tasks:pending"
        self.processing_key = "tasks:processing"
        self.failed_key = "tasks:failed"
        self.completed_key = "tasks:completed"

    def enqueue(self, task_data):
        task = {
            "id": str(uuid.uuid4()),
            "data": task_data,
            "enqueued_at": datetime.now().isoformat(),
            "attempts": 0
        }
        self.redis.lpush(self.queue_key, json.dumps(task))
        print(f"[Queue] Enqueued task {task['id']}")
        return task["id"]

    def dequeue(self, worker_id):
        task_json = self.redis.execute_command(
            'BLMOVE',
            self.queue_key,
            f"{self.processing_key}:{worker_id}",
            'RIGHT',
            'LEFT',
            5
        )
        if task_json:
            task = json.loads(task_json)
            task["attempts"] += 1
            task["worker_id"] = worker_id
            task["started_at"] = datetime.now().isoformat()
            return task
        return None

    def complete(self, worker_id, task):
        self.redis.lrem(f"{self.processing_key}:{worker_id}", 1, json.dumps(task))
        task["completed_at"] = datetime.now().isoformat()
        task["status"] = "completed"
        self.redis.lpush(self.completed_key, json.dumps(task))
        print(f"[Queue] Task {task['id']} completed")

    def fail(self, worker_id, task, error):
        self.redis.lrem(f"{self.processing_key}:{worker_id}", 1, json.dumps(task))
        task["failed_at"] = datetime.now().isoformat()
        task["status"] = "failed"
        task["error"] = str(error)
        if task["attempts"] < 3:
            print(f"[Queue] Task {task['id']} failed, retrying (attempt {task['attempts']})")
            self.redis.lpush(self.queue_key, json.dumps(task))
        else:
            print(f"[Queue] Task {task['id']} permanently failed after 3 attempts")
            self.redis.lpush(self.failed_key, json.dumps(task))

    def stats(self):
        return {
            "pending": self.redis.llen(self.queue_key),
            "failed": self.redis.llen(self.failed_key),
            "completed": self.redis.llen(self.completed_key)
        }