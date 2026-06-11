from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from strawberry.fastapi import GraphQLRouter
from .database import engine, SessionLocal, Base
from .models import Appointment
from .graphql_schema import schema

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Appointment Database Service")

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


@app.put("/appointments/{appointment_id}")
def update_appointment(appointment_id: int, time: str, db: Session = Depends(get_db)):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    appointment.time = time
    db.commit()
    db.refresh(appointment)
    return appointment


@app.delete("/appointments/{appointment_id}")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    db.delete(appointment)
    db.commit()
    return {"message": "Appointment deleted successfully", "appointment_id": appointment_id}


graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")
