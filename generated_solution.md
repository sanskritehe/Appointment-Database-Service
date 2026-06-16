### FILE: app/graphql_schema.py
```python
import strawberry
from typing import Optional
from app.database import SessionLocal
from app.models import Appointment as AppointmentModel


@strawberry.federation.type(keys=["id"])
class AppointmentStorage:
    id: int
    user: str
    time: str
    status: str


@strawberry.type
class Query:
    @strawberry.field
    def appointment_records(self) -> list[AppointmentStorage]:
        db = SessionLocal()
        try:
            rows = db.query(AppointmentModel).all()
            return [AppointmentStorage(id=r.id, user=r.user, time=r.time, status=r.status) for r in rows]
        finally:
            db.close()

    @strawberry.field
    def appointment_record(self, id: int) -> Optional[AppointmentStorage]:
        db = SessionLocal()
        try:
            r = db.query(AppointmentModel).filter(AppointmentModel.id == id).first()
            if r:
                return AppointmentStorage(id=r.id, user=r.user, time=r.time, status=r.status)
            return None
        finally:
            db.close()

    @strawberry.field
    def appointment_by_id(self, id: int) -> Optional[AppointmentStorage]:
        db = SessionLocal()
        try:
            r = db.query(AppointmentModel).filter(AppointmentModel.id == id).first()
            if r:
                return AppointmentStorage(id=r.id, user=r.user, time=r.time, status=r.status)
            return None
        finally:
            db.close()


@strawberry.type
class Mutation:
    @strawberry.mutation
    def store_appointment(self, user: str, time: str) -> AppointmentStorage:
        db = SessionLocal()
        try:
            record = AppointmentModel(user=user, time=time)
            db.add(record)
            db.commit()
            db.refresh(record)
            return AppointmentStorage(id=record.id, user=record.user, time=record.time, status=record.status)
        finally:
            db.close()

    @strawberry.mutation
    def remove_appointment(self, id: int) -> bool:
        db = SessionLocal()
        try:
            record = db.query(AppointmentModel).filter(AppointmentModel.id == id).first()
            if record:
                db.delete(record)
                db.commit()
                return True
            return False
        finally:
            db.close()


schema = strawberry.federation.Schema(query=Query, mutation=Mutation, enable_federation_2=True)

```

### FILE: app/models.py
```python
from sqlalchemy import Column, Integer, String
from .database import Base

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(String, index=True)
    time = Column(String)
    status = Column(String, default="booked")
```

### FILE: tests/test_graphql.py
```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_appointment_by_id_found(client):
    # Create a test appointment
    response = client.post("/graphql", json={
        "query": """
            mutation {
                storeAppointment(user: "test_user", time: "test_time") {
                    id
                    user
                    time
                    status
                }
            }
        """
    })
    appointment_id = response.json()["data"]["storeAppointment"]["id"]

    # Query the appointment by ID
    response = client.post("/graphql", json={
        "query": f"""
            query {
                appointmentById(id: {appointment_id}) {
                    id
                    user
                    time
                    status
                }
            }
        """
    })
    assert response.json()["data"]["appointmentById"] is not None

def test_appointment_by_id_not_found(client):
    # Query a non-existent appointment by ID
    response = client.post("/graphql", json={
        "query": """
            query {
                appointmentById(id: 99999) {
                    id
                    user
                    time
                    status
                }
            }
        """
    })
    assert response.json()["data"]["appointmentById"] is None
```