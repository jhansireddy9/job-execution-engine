# Resumable Job Execution Engine

## Overview

This project is a simple backend system to handle long-running jobs.
It allows users to submit jobs, track their status, cancel them, and ensures that jobs are not lost even if something goes wrong (like a crash).

The main goal of this project was to focus on **correctness and reliability**, rather than just making something that works in ideal conditions.


## What I Built

### Core Functionality

* Create jobs using an API
* Background worker that processes jobs
* Track job status (QUEUED → RUNNING → COMPLETED / FAILED / CANCELLED)


### Reliability Features

* **Retry mechanism**
  If a job fails, it is retried up to a limit

* **Stuck job recovery**
  If a job is stuck in RUNNING (e.g., worker crash), it is automatically re-queued

* **Priority handling**
  Jobs with higher priority are picked first (among queued jobs)

* **Cancellation support**
  Jobs can be cancelled while running

* **Controlled execution**
  Only one job runs at a time to avoid race conditions


## Level 3 (Agent Planning)

I added a simple endpoint:

```
POST /agent/plan
```

This takes a natural language instruction and converts it into a sequence of tasks with dependencies.

### Example:

Input:

```
run simulation then process results then generate report
```

Output:

```
[
  run_simulation → process_results → generate_report
]
```

This is a simplified version of a DAG (Directed Acyclic Graph), where each step depends on the previous one.

---

## Design Decisions

* I used a **simple async worker loop** instead of tools like Celery or Redis
  → This keeps the system easy to understand and control

* All job state is stored in the database
  → So jobs are not lost even if the system crashes

* I used **non-preemptive scheduling**
  → Once a job starts, it is not interrupted
  → Priority only affects queued jobs

* I intentionally kept the system simple rather than overengineering

---

## Failure Handling

* If a worker crashes → stuck jobs are detected and retried
* If a job fails → retried up to max limit
* Duplicate execution is avoided using job state

---

## How to Run

1. Install dependencies:

```
pip install -r requirements.txt
```

2. Start server:

```
uvicorn app.main:app --reload
```

3. Open:

```
http://127.0.0.1:8000/docs
```

---

## Example APIs

* Create job:

```
POST /jobs?priority=10
```

* Get status:

```
GET /jobs/{job_id}
```

* Cancel job:

```
POST /jobs/{job_id}/cancel
```

* Generate plan:

```
POST /agent/plan
```

---

## LLM Usage

I used ChatGPT during development to:

* understand system design concepts (workers, retries, etc.)
* debug async issues
* think through failure scenarios

All final code and logic were implemented and tested manually.

---

## What I Would Improve

If I had more time, I would:

* extend this into a full DAG execution system
* allow multiple workers (parallel processing)
* use Redis/Celery for distributed execution
* add better logging and monitoring

---

## Final Thoughts

This project helped me understand how real backend systems handle failures and long-running tasks.
I focused on making the system reliable and easy to reason about rather than adding unnecessary complexity.
