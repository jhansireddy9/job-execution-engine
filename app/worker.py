import asyncio
from datetime import datetime
from .database import SessionLocal
from .models import Job
is_processing = False
async def worker_loop():
    global is_processing

    print("Worker loop running...")

    while True:
        if is_processing:
            await asyncio.sleep(1)
            continue

        db = SessionLocal()

        job = db.query(Job)\
            .filter(Job.status == "QUEUED")\
            .order_by(Job.priority.desc())\
            .first()

        if job:
            is_processing = True

            print(f"Starting job {job.id}")
            print(f"Processing job {job.id} with priority {job.priority}")

            job.status = "RUNNING"
            db.commit()

            try:
                for i in range(5):
                    print(f"Processing {job.id} step {i+1}")
                    await asyncio.sleep(1)

                job.status = "COMPLETED"
                print(f"Job completed {job.id}")

            except Exception:
                job.retry_count += 1
                job.status = "FAILED"

            db.commit()
            is_processing = False 

        db.close()
        await asyncio.sleep(1)