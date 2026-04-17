# Resumable Job Execution Engine

## Overview

This project is a backend system to handle long-running jobs reliably.
It allows users to create jobs, track their status, cancel them, and ensures jobs are not lost even if the system crashes.

The focus was on building a **correct and reliable system**, not just a working one.

---

## Setup Instructions

1. Install dependencies:
   pip install -r requirements.txt

2. Configure environment variables:
   Create a `.env` file and add:
   DATABASE_URL=postgresql://postgres:password@localhost:5432/jobdb

3. Run the server:
   uvicorn app.main:app --reload

4. Open API docs:
   http://127.0.0.1:8000/docs

---

## Features Implemented

### Level 1 (Core)

* Job creation and status tracking
* Background worker execution
* Job lifecycle management (QUEUED → RUNNING → COMPLETED / FAILED / CANCELLED)

---

### Level 2 (Reliability)

* Priority-based job scheduling
* Retry mechanism for failed jobs
* Stuck job recovery (detects and requeues jobs)
* Cancellation support
* Controlled execution (only one job at a time)

---

### Level 3 (Partial)

* Added `/agent/plan` endpoint
* Converts natural language instructions into a sequence of tasks
* Generates a simple dependency chain (linear workflow)

---

## Design Decisions

* Used a simple async worker instead of Celery/Redis to keep the system easy to understand
* Stored all job states in the database to ensure reliability
* Used non-preemptive scheduling (running jobs are not interrupted)
* Limited execution to one job at a time to avoid race conditions

---

## Failure Handling

* Worker crash → stuck jobs are detected and retried
* Job failure → retried up to max limit
* Duplicate execution avoided using job states

---

## Limitations

* Uses polling instead of a distributed queue
* Only supports a single worker (no parallel execution)
* Level 3 supports only linear task chains (not full DAG execution)

---

## LLM Usage

I used ChatGPT to:


I used ChatGPT as a support tool during development, mainly for:

* Debugging an issue where the worker was not running due to incorrect startup handling  
* Identifying and fixing blocking calls (`time.sleep`) by replacing them with `asyncio.sleep`  
* Understanding how to safely handle job retries and failure scenarios  
* Clarifying the behavior of priority scheduling, especially the difference between queued and running jobs  

All implementations were tested and adapted manually to fit the system design.
---

## What I Would Do Differently

With more time, I would:

* implement a full DAG-based execution system
* allow parallel task execution
* use Celery and Redis for distributed workers
* add monitoring and logging

---

## Final Thoughts

This project helped me understand how backend systems handle long-running tasks and failures.
The focus was on reliability, simplicity, and clear system behavior.
