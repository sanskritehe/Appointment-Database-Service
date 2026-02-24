from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import engine, SessionLocal, Base
from .models import Appointment

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/appointments")
def create_appointment(user: str, time: str, db: Session = Depends(get_db)):
    appointment = Appointment(user=user, time=time)
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment

@app.get("/appointments")
def get_appointments(db: Session = Depends(get_db)):
    return db.query(Appointment).all()