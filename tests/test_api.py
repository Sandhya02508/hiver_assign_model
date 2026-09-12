from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Hiver Uber Support Agent" in response.text

def test_support_endpoint():
    response = client.post("/v1/support", json={"message": "My card was charged for a trip I never took."})
    assert response.status_code == 200
    data = response.json()
    assert "predicted_intent" in data
    assert "reply" in data
    assert "escalate" in data

def test_safety_escalation_endpoint():
    response = client.post("/v1/support", json={"message": "I was involved in an accident during my Uber trip."})
    assert response.status_code == 200
    data = response.json()
    assert data["escalate"] is True
    assert "safety" in data["escalation_reason"].lower() or "accident" in data["escalation_reason"].lower()

def test_evaluate_endpoint():
    response = client.post("/v1/evaluate")
    assert response.status_code == 200
    data = response.json()
    assert "total_test_cases" in data
