from fastapi import FastAPI
from app.database import engine, Base
from app.routes import patient_routes

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(patient_routes.router, prefix="/patients", tags=["Patients"])

@app.get("/")
def health_check():
    return {"message": "System up"}

