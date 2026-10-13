from database import engine,Base
from models import Job

Base.metadata.create_all(bind=engine)

print("Database tables created!")