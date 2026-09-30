from fastapi import FastAPI
from pydantic import BaseModel

from webhook import send_job_completed_webhook


app = FastAPI(
    title="Job Status Webhook API",
    description="Simple webhook system for job completion events",
    version="1.0"
)


# -----------------------------
# Data models
# -----------------------------

class WebhookRequest(BaseModel):
    webhook_url: str
    job_id: int
    customer_id: int


class JobCompletedEvent(BaseModel):
    event: str
    job_id: int
    customer_id: int


# -----------------------------
# Home
# -----------------------------

@app.get("/")
def home():
    return {
        "message": "Job Status Webhook API is running"
    }


# -----------------------------
# Receive webhook
# -----------------------------

@app.post("/webhooks/job-completed")
def receive_job_completed_webhook(
    event: JobCompletedEvent
):
    print("Webhook received!")
    print(event.model_dump())

    return {
        "message": "Webhook received successfully",
        "event": event.event,
        "job_id": event.job_id,
        "customer_id": event.customer_id
    }


# -----------------------------
# Send webhook
# -----------------------------

@app.post("/jobs/complete")
async def complete_job(
    request: WebhookRequest
):
    result = await send_job_completed_webhook(
        webhook_url=request.webhook_url,
        job_id=request.job_id,
        customer_id=request.customer_id
    )

    return {
        "message": "Job completed and webhook sent",
        "job_id": request.job_id,
        "customer_id": request.customer_id,
        "webhook_result": result
    }