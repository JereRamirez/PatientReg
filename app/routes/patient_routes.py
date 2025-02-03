from fastapi import APIRouter, Depends, UploadFile, File, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services import patient_service
from app.schemas.patient import PatientCreate, PatientResponse
from app.services.notification_service import get_notification_service, NotificationService

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model= PatientResponse, status_code=status.HTTP_201_CREATED)
async def create_patient(patient: PatientCreate = Depends(), dni_photo: UploadFile = File(...),
                   db: Session = Depends(get_db), notifier: NotificationService = Depends(get_notification_service)):
    new_patient = patient_service.create_patient(db, patient, dni_photo)
    await notifier.send(new_patient, channels=["email", "sms"])
    return new_patient
