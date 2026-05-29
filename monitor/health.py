import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from broker.queue import TaskQueue
import time

def monitor():
    queue = TaskQueue()
    print("=== Task Queue Monitor ===")
    print("Watching queue stats every 2 seconds...\n")
    
    while True:
        stats = queue.stats()
        print(f"[{time.strftime('%H:%M:%S')}] "
              f"Pending: {stats['pending']} | "
              f"Completed: {stats['completed']} | "
              f"Failed: {stats['failed']}")
        time.sleep(2)

if __name__ == "__main__":
    monitor()