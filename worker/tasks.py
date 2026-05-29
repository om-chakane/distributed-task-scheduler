import time
import random

def process_task(task_id, task_data):
    print(f"[Task {task_id[:8]}] Starting: {task_data}")
    
    duration = random.randint(1, 5)
    time.sleep(duration)
    
    # 20% chance of failure to simulate real-world crashes
    if random.random() < 0.2:
        raise Exception(f"Task crashed after {duration}s")
    
    print(f"[Task {task_id[:8]}] Done in {duration}s")
    return {"duration": duration, "status": "completed"}