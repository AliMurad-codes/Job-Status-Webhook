import httpx


async def send_job_completed_webhook(
    webhook_url: str,
    job_id: int,
    customer_id: int
):
    payload = {
        "event": "job.completed",
        "job_id": job_id,
        "customer_id": customer_id
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            webhook_url,
            json=payload
        )

    return {
        "status_code": response.status_code,
        "response": response.text
    }