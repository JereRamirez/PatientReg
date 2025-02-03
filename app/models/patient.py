from app.database import Base
from sqlalchemy import Column, Integer, String

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email_address = Column(String, unique=True, nullable=False)
    phone_number = Column(String, nullable=False)
    dni_photo_url = Column(String, nullable=True)