from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
import uuid

class Job(Base):
    __tablename__="jobs"


    id = Column(Integer, primary_key=True, index=True)
    course_name = Column(String, nullable=False)
    total_recipients = Column(Integer, nullable=False)
    status = Column(String, default="pending")

class Recipient(Base):
    __tablename__="recipients"

    id = Column(Integer, primary_key=True, index = True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    name = Column(String, nullable = False)
    email = Column(String, nullable = False)
    certificate_id = Column(
    String,
    unique=True,
    nullable=False,
    default=lambda: str(uuid.uuid4())
)
    status = Column(String, default="pending")