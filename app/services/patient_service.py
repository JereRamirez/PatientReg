from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException
from app.schemas.patient import PatientCreate
from app.services import file_service
from app.models.patient import Patient
import logging

logger = logging.getLogger(__name__)

def create_patient(db: Session, patient_data: PatientCreate, dni_photo: UploadFile):
    file_url = file_service.save_file(dni_photo)
    if not file_url:
        raise HTTPException(status_code=500, detail="Failed to upload file")

    new_patient = Patient(
        name=patient_data.name,
        email_address=str(patient_data.email_address),
        phone_number=patient_data.phone_number,
        dni_photo_url=file_url
    )

    try:
        db.add(new_patient)
        db.commit()
        db.refresh(new_patient)
    except Exception as e:
        db.rollback()
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error while creating patient")

    return new_patient