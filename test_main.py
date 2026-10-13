from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Bulk Certificate Generator API is running"
    }
def test_create_bulk_job():
    response = client.post(
        "/certificates",
        json={
            "course_name": "Python Programming",
            "recipients": [
                {
                    "name": "Test Arun",
                    "email": "arun.test@example.com"
                },
                {
                    "name": "Test Priya",
                    "email": "priya.test@example.com"
                }
            ]
        }
    )

    assert response.status_code == 200

    data = response.json()
    assert data["total_recipients"] == 2
    assert "job_id" in data

def test_invalid_email():
    response = client.post(
        "/certificates",
        json={
            "course_name": "Python Programming",
            "recipients": [
                {
                    "name": "Test User",
                    "email": "not-an-email"
                }
            ]
        }
    )

    assert response.status_code == 422


def test_download_certificate():
    create_response = client.post(
        "/certificates",
        json={
            "course_name": "Python Programming",
            "recipients": [
                {
                    "name": "Download Test",
                    "email": "download.test@example.com"
                }
            ]
        }
    )

    assert create_response.status_code == 200

    job_id = create_response.json()["job_id"]

    recipients_response = client.get(
        f"/certificates/{job_id}/recipients"
    )

    assert recipients_response.status_code == 200

    recipient_id = recipients_response.json()[0]["id"]

    print("Recipient ID:", recipient_id)


    download_response = client.get(
        f"/certificates/recipient/{recipient_id}/download"
    )

    print("Download status:", download_response.status_code)
    print("Download response:", download_response.text)

    assert download_response.status_code == 200
    assert download_response.headers["content-type"] == "application/pdf"

def test_job_status():
    create_response = client.post(
        "/certificates",
        json={
            "course_name": "Python Programming",
            "recipients": [
                {
                    "name": "Status Test",
                    "email": "status.test@example.com"
                }
            ]
        }
    )

    assert create_response.status_code == 200
    job_id = create_response.json()["job_id"]

    response = client.get(
        f"/certificates/{job_id}/status"
    )

    assert response.status_code == 200

    data = response.json()
    assert data["job_id"] == job_id
    assert data["total_recipients"] == 1
    assert data["successful"] + data["failed"] == 1
    assert data["progress_percentage"] == 100


def test_verify_valid_certificate():
    create_response = client.post(
        "/certificates",
        json={
            "course_name": "Python Programming",
            "recipients": [
                {
                    "name": "Verification Test",
                    "email": "verify.test@example.com"
                }
            ]
        }
    )

    assert create_response.status_code == 200

    job_id = create_response.json()["job_id"]

    recipients_response = client.get(
        f"/certificates/{job_id}/recipients"
    )

    recipient_id = recipients_response.json()[0]["id"]

    # Read the certificate ID from the database-backed model
    from main import get_db
    from models import Recipient

    db = next(get_db())
    try:
        recipient = db.query(Recipient).filter(
            Recipient.id == recipient_id
        ).first()
        certificate_id = recipient.certificate_id
    finally:
        db.close()

    response = client.get(
        f"/certificates/verify/{certificate_id}"
    )

    assert response.status_code == 200
    assert response.json()["valid"] is True


def test_verify_invalid_certificate():
    response = client.get(
        "/certificates/verify/invalid-certificate-id"
    )

    assert response.status_code == 404
