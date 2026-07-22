import io
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_predict_rejects_invalid_file_type():
    fake_file = io.BytesIO(b"not an image")
    response = client.post(
        "/predict",
        files={"file": ("test.txt", fake_file, "text/plain")}
    )
    assert response.status_code == 400

def test_predict_valid_image():
    with open("tests/test_leaf.jpg", "rb") as f:
        response = client.post(
            "/predict",
            files={"file": ("test_leaf.jpg", f, "image/jpeg")}
        )
    assert response.status_code == 200
    data = response.json()
    assert "disease" in data
    assert "confidence" in data
    assert "treatment_tip" in data
