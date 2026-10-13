
from certificate_generator import generate_certificate
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi.responses import FileResponse
import os

from schemas import BulkCertificateRequest
from database import SessionLocal
from models import Job, Recipient

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {
        "message": "Bulk Certificate Generator API is running"
    }


@app.post("/certificates")
def create_certificates(
    request: BulkCertificateRequest,
    db: Session = Depends(get_db)
):
    # Create a job for this bulk request
    job = Job(
        course_name=request.course_name,
        total_recipients=len(request.recipients),
        status="pending"
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    # Process each recipient
    for recipient in request.recipients:
        new_recipient = Recipient(
            job_id=job.id,
            name=recipient.name,
            email=recipient.email,
            status="pending"
        )

        db.add(new_recipient)
        db.commit()
        db.refresh(new_recipient)

        # Generate the recipient's PDF
        try:
            generate_certificate(
                name=new_recipient.name,
                certificate_id=new_recipient.certificate_id,
                course_name=job.course_name,
                recipient_id=new_recipient.id
            )
            new_recipient.status = "success"

        except Exception as e:
            print(
                f"Certificate generation failed for "
                f"{new_recipient.email}: {e}"
            )
            new_recipient.status = "failed"

        db.commit()

    # Update the job after all recipients are processed
    recipients = (
        db.query(Recipient)
        .filter(Recipient.job_id == job.id)
        .all()
    )

    if all(r.status == "success" for r in recipients):
        job.status = "completed"
    elif all(r.status == "failed" for r in recipients):
        job.status = "failed"
    else:
        job.status = "partially_completed"

    db.commit()

    return {
        "job_id": job.id,
        "course_name": job.course_name,
        "total_recipients": job.total_recipients,
        "status": job.status
    }


@app.get("/certificates/{job_id}/recipients")
def get_recipients(
    job_id: int,
    db: Session = Depends(get_db)
):
    recipients = (
        db.query(Recipient)
        .filter(Recipient.job_id == job_id)
        .all()
    )

    return [
        {
            "id": recipient.id,
            "name": recipient.name,
            "email": recipient.email,
            "status": recipient.status
        }
        for recipient in recipients
    ]

@app.get("/certificates/recipient/{recipient_id}/download")
def download_certificate(
    recipient_id: int,
    db: Session = Depends(get_db)
):
    recipient = (
        db.query(Recipient)
        .filter(Recipient.id == recipient_id)
        .first()
    )

    if recipient is None:
        raise HTTPException(
            status_code=404,
            detail="Recipient not found"
        )

    file_path = f"certificates/certificate_{recipient.id}.pdf"

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="Certificate file not found"
        )

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=f"certificate_{recipient.id}.pdf"
    )


@app.get("/certificates/{job_id}/status")
def get_job_status(
    job_id: int,
    db: Session = Depends(get_db)
):
    job = db.query(Job).filter(Job.id == job_id).first()

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    recipients = (
        db.query(Recipient)
        .filter(Recipient.job_id == job_id)
        .all()
    )

    successful = sum(
        1 for r in recipients if r.status == "success"
    )
    failed = sum(
        1 for r in recipients if r.status == "failed"
    )

    completed = successful + failed

    progress = (
        completed / job.total_recipients * 100
        if job.total_recipients > 0
        else 0
    )

    return {
        "job_id": job.id,
        "status": job.status,
        "total_recipients": job.total_recipients,
        "successful": successful,
        "failed": failed,
        "progress_percentage": progress
    }


@app.get("/certificates/verify/{certificate_id}")
def verify_certificate(
    certificate_id: str,
    db: Session = Depends(get_db)
):
    recipient = (
        db.query(Recipient)
        .filter(Recipient.certificate_id == certificate_id)
        .first()
    )

    if recipient is None:
        raise HTTPException(
            status_code=404,
            detail="Certificate not found or invalid"
        )

    return {
        "valid": True,
        "certificate_id": recipient.certificate_id,
        "recipient_name": recipient.name,
        "course_name": db.query(Job)
            .filter(Job.id == recipient.job_id)
            .first().course_name
    }
