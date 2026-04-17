from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import asyncio
from .database import Base, engine, SessionLocal
from .models import Job
from .worker import worker_loop

app = FastAPI()
@app.on_event("startup")
async def start_worker():
    print("🚀 Starting worker...")   # 👈 add this
    asyncio.create_task(worker_loop())
# create tables
Base.metadata.create_all(bind=engine)


# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create Job
@app.post("/jobs")
def create_job(priority: int = 1,db: Session = Depends(get_db)):
    job = Job(priority=priority)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


# Get Job Status
@app.get("/jobs/{job_id}")
def get_job(job_id: str, db: Session = Depends(get_db)):
    return db.query(Job).filter(Job.id == job_id).first()


# Cancel Job
@app.post("/jobs/{job_id}/cancel")
def cancel_job(job_id: str, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if job:
        job.cancel_requested = True
        db.commit()
    return {"message": "cancel requested"}


# Start Worker
@app.on_event("startup")
async def start_worker():
    asyncio.create_task(worker_loop())

@app.post("/agent/plan")
def generate_plan(instruction: str):
    steps = instruction.lower().split("then")

    plan = []
    prev = None

    for step in steps:
        task_name = step.strip().replace(" ", "_")

        plan.append({
            "task": task_name,
            "depends_on": [prev] if prev else []
        })

        prev = task_name

    return plan