import io
import pytest
from fastapi.testclient import TestClient
from api import app  # Import your FastAPI app
from api import TEMPLATE_PATHS  # Import required variables

client = TestClient(app)

# Mock authentication function (if needed)
def mock_verify_passcode():
    return "test_user"

@pytest.fixture
def valid_image():
    return io.BytesIO(b"valid_image_data")

def test_health_check():
    """Test if the API is running."""
    response = client.get("/")
    assert response.status_code == 200

def test_upload_valid_image(valid_image):
    """Test uploading a valid image with a correct template."""
    files = {"file": ("test.png", valid_image, "image/png")}
    data = {"template_name": list(TEMPLATE_PATHS.keys())[0], "username": "test_user"}

    response = client.post("/analyze_diagram", files=files, data=data)
    assert response.status_code == 200
    assert "response" in response.json()
    assert "prompt" in response.json()

def test_upload_invalid_template(valid_image):
    """Test uploading an image with an invalid template name."""
    files = {"file": ("test.png", valid_image, "image/png")}
    data = {"template_name": "Invalid Template", "username": "test_user"}

    response = client.post("/analyze_diagram", files=files, data=data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid template selected"

def test_upload_missing_file():
    """Test request without an image file."""
    data = {"template_name": list(TEMPLATE_PATHS.keys())[0], "username": "test_user"}

    response = client.post("/analyze_diagram", data=data)
    assert response.status_code == 422  # Unprocessable Entity

def test_upload_without_authentication(valid_image):
    """Test unauthorized access without a username."""
    files = {"file": ("test.png", valid_image, "image/png")}
    data = {"template_name": list(TEMPLATE_PATHS.keys())[0]}

    response = client.post("/analyze_diagram", files=files, data=data)
    assert response.status_code == 401  # Unauthorized
