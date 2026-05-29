from broker.queue import TaskQueue
import time

def main():
    queue = TaskQueue()
    
    print("=== Distributed Task Scheduler ===")
    print("Enqueuing 10 tasks...\n")
    
    # Enqueue 10 tasks
    for i in range(10):
        queue.enqueue(f"task-payload-{i}")
        time.sleep(0.1)
    
    print(f"\nStats: {queue.stats()}")
    print("\nNow start workers in separate terminals to process these tasks.")
    print("Run: python -m worker.worker worker-1")

if __name__ == "__main__":
    main()