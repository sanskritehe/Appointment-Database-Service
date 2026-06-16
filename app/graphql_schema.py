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

