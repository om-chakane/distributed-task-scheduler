import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from broker.queue import TaskQueue
from worker.tasks import process_task

class Worker:
    def __init__(self, worker_id):
        self.worker_id = worker_id
        self.queue = TaskQueue()
        self.running = True
        print(f"[Worker {self.worker_id}] Started, waiting for tasks...")

    def run(self):
        while self.running:
            try:
                task = self.queue.dequeue(self.worker_id)
                if task:
                    try:
                        result = process_task(task["id"], task["data"])
                        self.queue.complete(self.worker_id, task)
                    except Exception as e:
                        print(f"[Worker {self.worker_id}] Task failed: {e}")
                        self.queue.fail(self.worker_id, task, e)
            except Exception as e:
                print(f"[Worker {self.worker_id}] Connection error, retrying: {e}")
                import time
                time.sleep(2)

if __name__ == "__main__":
    worker_id = sys.argv[1] if len(sys.argv) > 1 else "worker-1"
    worker = Worker(worker_id)
    worker.run()