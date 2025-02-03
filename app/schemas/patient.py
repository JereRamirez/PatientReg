from pydantic import BaseModel, EmailStr, field_validator, ValidationError
from phonenumbers import parse, is_valid_number
from phonenumbers.phonenumberutil import NumberParseException

class PatientCreate(BaseModel):
    name: str
    email_address: EmailStr
    phone_number: str

    @field_validator('phone_number')
    def validate_phone_number(cls, value):
        try:
            parsed_number = parse(value, None)
            if not is_valid_number(parsed_number):
                raise ValueError('Invalid phone number')
            return value
        except (NumberParseException, ValueError):
            raise ValueError('Invalid phone number format')

class PatientResponse(PatientCreate):
    id: int
    dni_photo_url: str | None = None

    class Config:
        orm_mode = True