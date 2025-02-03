import pytest
from fastapi import UploadFile, HTTPException
from io import BytesIO
from sqlalchemy.orm import Session
from app.schemas.patient import PatientCreate
from app.services import patient_service
from sqlalchemy.exc import SQLAlchemyError

@pytest.fixture
def mock_db(mocker):
    db = mocker.MagicMock(spec=Session)
    return db

@pytest.fixture
def mock_file_service(mocker):
    return mocker.patch("app.services.file_service.save_file", return_value="fake_url")

@pytest.fixture
def fake_dni_photo():
    return UploadFile(filename="dni.jpg", file=BytesIO(b"fake image data"))

@pytest.fixture
def patient_data():
    return PatientCreate(
        name="John Doe",
        email_address="john.doe@example.com",
        phone_number="+442083661177"
    )

def test_create_patient(mock_db, mock_file_service, fake_dni_photo, patient_data):
    new_patient = patient_service.create_patient(mock_db, patient_data, fake_dni_photo)

    assert new_patient.name == patient_data.name
    assert new_patient.email_address == str(patient_data.email_address)
    assert new_patient.phone_number == patient_data.phone_number
    assert new_patient.dni_photo_url == "fake_url"

    mock_db.add.assert_called_once_with(new_patient)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(new_patient)

    mock_file_service.assert_called_once_with(fake_dni_photo)

def test_create_patient_file_save_error(mock_db, mocker, fake_dni_photo, patient_data):
    mocker.patch("app.services.file_service.save_file", side_effect=Exception("File save failed"))

    with pytest.raises(Exception, match="File save failed"):
        patient_service.create_patient(mock_db, patient_data, fake_dni_photo)

def test_create_patient_with_missing_dni_photo(mock_db, patient_data):
    with pytest.raises(AttributeError):
        patient_service.create_patient(mock_db, patient_data, None)

def test_create_patient_with_db_failure(mock_db, mock_file_service, fake_dni_photo, patient_data):
    mock_db.add.side_effect = SQLAlchemyError("Database error during insert")

    with pytest.raises(HTTPException) as exc_info:
        patient_service.create_patient(mock_db, patient_data, fake_dni_photo)

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "Database error while creating patient"

    mock_file_service.assert_called_once_with(fake_dni_photo)

    mock_db.commit.assert_not_called()
    mock_db.refresh.assert_not_called()