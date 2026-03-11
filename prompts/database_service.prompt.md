# Appointment Database Service – API Implementation Prompt

You are an AI development agent working on the **Appointment-Database-Service** repository.

Your task is to implement and maintain database APIs for managing appointment records.

---

# Goal

Implement APIs that allow the system to:

* Create new appointments
* Retrieve existing appointments
* Delete appointments

This service acts as the **data persistence layer** for the appointment system.

The APIs will be consumed by the **Appointment-Service**, which contains the business logic layer.

---

# Technology Stack

The implementation must follow these technologies:

* **FastAPI** for building REST APIs
* **SQLAlchemy ORM** for database interaction
* **SQLite** as the database engine
* **Python dependency injection** using FastAPI `Depends`

Database file:

appointments.db

---

# Database Configuration

The database connection is defined in **database.py**.

The database URL must be:

sqlite:///./appointments.db

The engine must be created using:

* `create_engine`
* `connect_args={"check_same_thread": False}`

Database sessions must be created using:

SessionLocal = sessionmaker(bind=engine)

The base class for ORM models must be:

Base = declarative_base()

---

# Data Model

Appointments are stored using a SQLAlchemy model.

Table name:

appointments

Fields:

id

* Integer
* Primary Key
* Auto Increment

user

* String
* Represents the user booking the appointment

time

* String
* Represents the appointment time slot

status

* String
* Default value: "booked"

Example model structure:

class Appointment(Base):
**tablename** = "appointments"

```
id = Column(Integer, primary_key=True, index=True)
user = Column(String, index=True)
time = Column(String)
status = Column(String, default="booked")
```

---

# Database Initialization

When the application starts, ensure that database tables are created using:

Base.metadata.create_all(bind=engine)

---

# Dependency Injection

Database sessions must be accessed using FastAPI dependency injection.

Use the following pattern:

db: Session = Depends(get_db)

The `get_db()` function should:

* Create a database session using SessionLocal
* Yield the session
* Close the session after the request finishes

---

# APIs to Implement

## 1. Create Appointment

Endpoint:

POST /appointments

Purpose:

Create a new appointment in the database.

Flow:

1. Accept `user` and `time` parameters.
2. Create an Appointment object.
3. Set default status to `"booked"`.
4. Insert the record into the database.
5. Commit the transaction.
6. Refresh the object.
7. Return the created appointment.

Expected behavior:

* The appointment should be persisted in SQLite.
* Return the inserted record as JSON.

---

## 2. Get All Appointments

Endpoint:

GET /appointments

Purpose:

Fetch all appointments stored in the database.

Flow:

1. Query the appointments table.
2. Retrieve all records.
3. Return the list as JSON.

Expected behavior:

Return a list of appointment objects.

---

## 3. Delete Appointment

Endpoint:

DELETE /appointments/{appointment_id}

Purpose:

Remove an appointment from the database.

Flow:

1. Query the appointment using the provided ID.
2. If the appointment does not exist:

   * Raise HTTPException with status code **404**.
3. Delete the appointment from the database.
4. Commit the transaction.
5. Return a confirmation response.

Example response:

{
"message": "Appointment deleted successfully",
"appointment_id": 5
}

---

# Error Handling

If an appointment is not found, raise:

HTTPException(status_code=404, detail="Appointment not found")

Ensure proper JSON responses are returned.

---

# Project Structure

Follow the existing repository structure.

app/

database.py

* database engine configuration
* session management

models.py

* SQLAlchemy models

main.py

* FastAPI application
* API routes

---

# Implementation Rules

* Follow FastAPI best practices.
* Use SQLAlchemy ORM queries for all database operations.
* Use dependency injection for database sessions.
* Return JSON responses for all APIs.
* Ensure proper error handling.
* Keep code modular and clean.

---

# After Implementation

Once the feature is implemented:

1. Create a new Git branch

feature/delete-appointment-db-api

2. Stage code changes

git add .

3. Commit the changes

git commit -m "Add delete appointment API for database service"

4. Push the branch

git push origin feature/delete-appointment-db-api

5. Create a Pull Request to merge into the main branch.

---

# Expected Outcome

After implementation:

* Appointment records can be created
* Appointment records can be retrieved
* Appointment records can be deleted
* The database service works correctly with the Appointment-Service
