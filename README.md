# Distributed Task Scheduler

A fault-tolerant distributed task queue built in Python with Redis, featuring 
multi-worker job processing, automatic failure recovery, and a real-time 
web dashboard.

## The Problem This Solves

In distributed systems, workers crash. Networks fail. Jobs get lost.
This system ensures that no task is ever lost — if a worker crashes 
mid-job, the task is automatically detected and reassigned to another 
worker. Jobs are retried up to 3 times before being marked as permanently 
failed.

## Architecture
```
Producer
    |
    v
  Redis (pending / processing / completed / failed)
    |
    |-----> Worker 1
    |-----> Worker 2
    |-----> Worker 3
                |
                v
          Dashboard (real-time monitoring)
```

## Key Features

- **Fault tolerance** — crashed workers don't lose tasks, jobs are 
  automatically reassigned
- **Atomic task pickup** — uses Redis BRPOPLPUSH to prevent two workers 
  from grabbing the same task simultaneously
- **Automatic retry** — failed tasks are retried up to 3 times before 
  being permanently failed
- **Multi-worker** — multiple workers run in parallel, each competing 
  for tasks independently
- **Real-time dashboard** — Flask web UI showing live queue stats, 
  completed tasks, and which worker handled each job

## Tech Stack

- **Python** — worker logic, task processing, broker
- **Redis** — queue backbone and shared state across workers
- **Flask** — web dashboard
- **Docker** — containerization (coming soon)

## Running Locally

**1. Start Redis:**
```bash
redis-server
```

**2. Activate virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install redis rq flask
```

**3. Enqueue tasks:**
```bash
python main.py
```

**4. Start workers (each in a separate terminal):**
```bash
python -m worker.worker worker-1
python -m worker.worker worker-2
python -m worker.worker worker-3
```

**5. Open dashboard:**
http://localhost:5001

## What I Learned

This project gave me hands-on experience with the open-source equivalents 
of distributed infrastructure tools I worked with at Meta — Redis as a 
shared state store (equivalent to ZippyDB), atomic queue operations for 
safe concurrent access, and real-time observability of a distributed system.

The core challenge was ensuring no task gets processed twice and no task 
gets lost when a worker crashes — solved using Redis's atomic BRPOPLPUSH 
operation to move tasks between queue states in a single step.