## 1. Project Overview

This repository implements the `appointment-database-service`.

Purpose:
- Handle persistence of appointment data.
- Expose REST APIs for storing and retrieving appointment records.
- Do NOT contain business logic.
- Do NOT perform cross-service validation logic.

This service:
- Uses FastAPI.
- Uses SQLAlchemy ORM.
- Uses SQLite (appointments.db).
- Exposes `/appointments` endpoints.

The Appointment Service will call this service via HTTP.

---

## 2. Architecture Rules

- This service is responsible ONLY for data storage and retrieval.
- Business logic (like double booking checks or workflow rules) must NOT be implemented here.
- This service must remain a pure data-access layer.
- Never directly communicate with other services.
- Never embed business logic inside database models.

---

## 3. Folder Structure

app/
    database.py   → DB connection and session
    models.py     → SQLAlchemy models
    main.py       → FastAPI routes

When adding new features:
- Modify models in `models.py`
- Add new endpoints in `main.py`
- Keep DB session handling consistent with existing pattern

---

## 4. Database Rules

- Use SQLAlchemy ORM.
- Use `Base` from database.py.
- Use proper column types.
- Use indexing where appropriate.
- Avoid raw SQL unless absolutely necessary.
- Preserve SQLite compatibility.

---

## 5. Model Conventions

Current model:

Appointment:
- id (Integer, Primary Key)
- user (String, Indexed)
- time (String)
- status (String, default="booked")

When extending the model:
- Add new fields as SQLAlchemy Columns.
- Maintain backward compatibility.
- Do not remove existing fields unless explicitly instructed.
- Use sensible defaults for new fields.

---

## 6. API Design Guidelines

- Use RESTful naming.
- Return ORM objects directly only if safe.
- Prefer JSON-serializable responses.
- Maintain consistency with existing endpoints:

POST   /appointments
GET    /appointments

When adding new endpoints:
- Follow same style and dependency injection pattern.
- Use FastAPI `Depends(get_db)` for DB access.

---

## 7. Error Handling

- Handle database errors gracefully.
- Return meaningful HTTP status codes.
- Do not expose internal DB errors in response.

---

## 8. Testing Expectations

When generating new features:
- Create test cases using pytest.
- Cover:
    - Successful creation
    - Query results
    - Edge cases
- Ensure DB session cleanup.

---

## 9. AI Behavior Rules

When modifying this repository:

1. Analyze existing code patterns before generating new code.
2. Do not refactor unrelated sections.
3. Avoid rewriting entire files unless required.
4. Preserve existing endpoints.
5. Add only the necessary minimal changes.
6. Ensure new code integrates with existing DB session logic.

---

## 10. Constraints

- This service must remain independent.
- Must not include HTTP calls to other services.
- Must not include business validation logic.
- Must not hardcode external URLs.