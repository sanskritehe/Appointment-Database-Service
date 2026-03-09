# Appointment Database Service – API Implementation Prompt

You are an AI development agent working on the **Appointment-Database-Service** repository.

## Goal

Implement database APIs to manage appointment records using SQLite.

This service is responsible for:

* Storing appointments
* Fetching appointments
* Deleting appointments

The service will be called by the **Appointment-Service**.

---

## Database

Use SQLite database:

appointments.db

Table structure:

appointments

* id (INTEGER PRIMARY KEY AUTOINCREMENT)
* user_id (TEXT)
* doctor_id (TEXT)
* time_slot (TEXT)
* status (TEXT)

---

## APIs to Implement

### 1. Create Appointment

POST /appointments

Flow:

1. Insert appointment into SQLite table
2. Set status = "booked"
3. Return inserted record

---

### 2. Get All Appointments

GET /appointments

Flow:

1. Fetch all rows from appointments table
2. Return list of appointments

---

### 3. Delete Appointment

DELETE /appointments/{appointment_id}

Flow:

1. Find appointment by ID
2. Update status to "cancelled" or remove record
3. Return confirmation response

---

## Implementation Guidelines

* Use FastAPI
* Use sqlite3 module
* Return JSON responses
* Handle errors if appointment does not exist

---

## Project Structure

app/
routes/
models/
database/

Add delete endpoint in the router handling appointments.

---

## After Implementation

1. Create new branch:
   feature/delete-appointment-db-api

2. Commit code changes

3. Push branch to GitHub

4. Create Pull Request
