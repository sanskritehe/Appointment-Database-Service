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
