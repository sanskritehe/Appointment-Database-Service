# Generic Database Service

You are an AI development agent working on a **Database Service repository**.

## Goal

Implement CRUD APIs for a resource using a relational database.
This service is responsible only for **data persistence**.

---

## Runtime Context (Provided Dynamically)

* Resource: {resource}
* Fields: {fields}
* Database URL: {database_url}

---

## Responsibilities

Implement:

* Create resource
* Read all resources
* Read resource by ID
* Update resource
* Delete resource

---

## Tech Stack

* FastAPI
* SQLAlchemy (ORM)
* Relational DB (SQLite or configured)

---

## APIs

### Create

POST /{resource}

* Insert record into DB
* Apply default values if needed
* Return created entity

---

### Read All

GET /{resource}

* Fetch all records
* Return list

---

### Read by ID

GET /{resource}/{id}

* Fetch single record
* Return 404 if not found

---

### Update

PUT /{resource}/{id}

* Update existing record
* Return updated entity

---

### Delete

DELETE /{resource}/{id}

* Delete or soft delete
* Return confirmation

Example:

```json
{
  "message": "Deleted successfully",
  "id": 1
}
```

---

## Architecture

app/
├─ models/
├─ database.py
└─ main.py

---

## Implementation Rules

* Use SQLAlchemy ORM
* Use dependency injection for DB session
* Validate input data
* Handle errors (404, invalid input)
* Return JSON responses

---

## Validation

* Ensure all CRUD APIs work
* Validate schema during create/update
* Handle missing records gracefully

---

## After Implementation

* Create feature branch
* Commit changes
* Push to repository
* Create Pull Request
