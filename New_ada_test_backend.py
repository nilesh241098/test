import pytest
from fastapi.testclient import TestClient
from main import app  # Import your FastAPI app
import os

client = TestClient(app)

# Helper function to load a valid test image
def load_test_image():
    test_image_path = os.path.join(os.path.dirname(__file__), "test.png")
    with open(test_image_path, "rb") as img_file:
        return img_file.read()

# ✅ 1. Test valid image and template
def test_valid_image_and_template():
    image_data = load_test_image()
    files = {"file": ("test.png", image_data, "image/png")}
    data = {"template_name": "General Architecture Review"}

    response = client.post("/analyze_diagram", files=files, data=data, auth=("test_user", "test_pass"))

    assert response.status_code == 200
    json_data = response.json()
    assert "response" in json_data
    assert "prompt" in json_data

# ❌ 2. Test invalid template name
def test_invalid_template():
    image_data = load_test_image()
    files = {"file": ("test.png", image_data, "image/png")}
    data = {"template_name": "Invalid Template"}

    response = client.post("/analyze_diagram", files=files, data=data, auth=("test_user", "test_pass"))

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid template name"

# ❌ 3. Test missing image file
def test_missing_image():
    data = {"template_name": "General Architecture Review"}

    response = client.post("/analyze_diagram", data=data, auth=("test_user", "test_pass"))

    assert response.status_code == 400

# ❌ 4. Test missing template name
def test_missing_template_name():
    image_data = load_test_image()
    files = {"file": ("test.png", image_data, "image/png")}

    response = client.post("/analyze_diagram", files=files, auth=("test_user", "test_pass"))

    assert response.status_code == 400

# ❌ 5. Test unauthorized access (No credentials)
def test_unauthorized_access():
    image_data = load_test_image()
    files = {"file": ("test.png", image_data, "image/png")}
    data = {"template_name": "General Architecture Review"}

    response = client.post("/analyze_diagram", files=files, data=data)  # No auth

    assert response.status_code == 401

# ❌ 6. Test invalid image format (Upload text file instead of an image)
def test_invalid_image_format():
    files = {"file": ("test.txt", b"This is not an image", "text/plain")}
    data = {"template_name": "General Architecture Review"}

    response = client.post("/analyze_diagram", files=files, data=data, auth=("test_user", "test_pass"))

    assert response.status_code == 400

# ❌ 7. Test large image file (Simulate large payload)
def test_large_image():
    large_image_data = b"\x89PNG\r\n" + b"A" * (5 * 1024 * 1024)  # 5MB fake image
    files = {"file": ("large_test.png", large_image_data, "image/png")}
    data = {"template_name": "General Architecture Review"}

    response = client.post("/analyze_diagram", files=files, data=data, auth=("test_user", "test_pass"))

    assert response.status_code == 413  # Payload Too Large

# ❌ 8. Test corrupted image file
def test_corrupted_image():
    corrupted_image_data = b"\x89PNG\r\nNOT_AN_IMAGE"
    files = {"file": ("corrupt.png", corrupted_image_data, "image/png")}
    data = {"template_name": "General Architecture Review"}

    response = client.post("/analyze_diagram", files=files, data=data, auth=("test_user", "test_pass"))

    assert response.status_code == 400

# ✅ 9. Test different valid templates
@pytest.mark.parametrize("template_name", [
    "Security Architecture Review",
    "Infrastructure Architecture Review",
    "Application Architecture Review",
    "Cloud Architecture Review",
])
def test_different_valid_templates(template_name):
    image_data = load_test_image()
    files = {"file": ("test.png", image_data, "image/png")}
    data = {"template_name": template_name}

    response = client.post("/analyze_diagram", files=files, data=data, auth=("test_user", "test_pass"))

    assert response.status_code == 200
    json_data = response.json()
    assert "response" in json_data
    assert "prompt" in json_data

# ✅ 10. Test response structure correctness
def test_response_structure():
    image_data = load_test_image()
    files = {"file": ("test.png", image_data, "image/png")}
    data = {"template_name": "General Architecture Review"}

    response = client.post("/analyze_diagram", files=files, data=data, auth=("test_user", "test_pass"))

    assert response.status_code == 200
    json_data = response.json()
    
    assert isinstance(json_data, dict)
    assert "response" in json_data
    assert "prompt" in json_data
    assert isinstance(json_data["response"], str)
    assert isinstance(json_data["prompt"], str)
