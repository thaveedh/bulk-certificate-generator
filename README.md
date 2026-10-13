# Bulk Certificate Generator

A Python-based web application that generates personalized PDF certificates in bulk using FastAPI, SQLite, SQLAlchemy, and ReportLab.

## Features

- Generate personalized certificates for multiple recipients.
- Store jobs and recipient details in SQLite.
- Generate PDF certificates with a professional navy-and-gold design.
- Download individual certificates.
- Track certificate generation job status.
- Verify certificates using unique certificate IDs.
- Validate recipient email addresses.
- Automated API tests using Pytest.

## Tech Stack

- Python
- FastAPI
- SQLite
- SQLAlchemy
- Pydantic
- ReportLab
- Pytest

## Prerequisites

- Python 3.10 or newer
- pip
- Git (optional, for cloning the repository)

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/thaveedh/bulk-certificate-generator/
cd bulk-certificate-generator
```

If you already downloaded the project, open a terminal in the project folder instead.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

```cmd
.venv\Scripts\activate.bat
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Initialize the database

```bash
python init_db.py
```

### 6. Start the application

```bash
uvicorn main:app --reload
```

The API will run locally at:

http://127.0.0.1:8000

### 7. Open the API documentation

Visit:

http://127.0.0.1:8000/docs

Use the interactive Swagger UI to try the API endpoints.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Check whether the API is running |
| POST | `/certificates` | Generate certificates in bulk |
| GET | `/certificates/{job_id}/recipients` | List recipients for a job |
| GET | `/certificates/recipient/{recipient_id}/download` | Download a recipient's certificate |
| GET | `/certificates/{job_id}/status` | Check job status |
| GET | `/certificates/verify/{certificate_id}` | Verify a certificate |

## Running Tests

Run the API test suite:

```bash
python -m pytest test_main.py -v
```

## Project Structure

```text
bulk-certificate-generator/
├── main.py
├── models.py
├── schemas.py
├── database.py
├── init_db.py
├── certificate_generator.py
├── test_main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Notes

- The SQLite database and generated PDF files are local runtime data.
- Keep secrets and API keys in `.env`; never commit that file to GitHub.
- The certificate design uses a fixed navy-and-gold layout.
