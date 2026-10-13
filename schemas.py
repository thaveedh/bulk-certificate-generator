# validation purpose

from pydantic import BaseModel, EmailStr

class Recipients(BaseModel):
    name: str
    email: EmailStr

class BulkCertificateRequest(BaseModel):
    course_name: str
    recipients: list[Recipients]