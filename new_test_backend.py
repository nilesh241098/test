from fastapi.testclient import TestClient
from main import app  # Replace with your FastAPI app file name
import pytest
from unittest.mock import patch
import json
from time import sleep

client = TestClient(app)

# Test 1: Successful Request with Valid Cloud Provider and Role (JSON)
def test_enumerator_api_success():
    """
    Test the /enumerator API with a valid cloud provider and JSON role data.
    """
    valid_json_role = json.dumps({"key": "value"})  # Any valid JSON structure
    response = client.post(
        "/enumerator",
        json={
            "cloud_provider": "AWS",
            "role": valid_json_role  # Role is JSON
        }
    )
    assert response.status_code == 200
    assert "response" in response.json()
    assert "hyperparameters" in response.json()


# Test 2: Missing Cloud Provider
def test_enumerator_api_missing_cloud_provider():
    """
    Test the /enumerator API when cloud provider is missing.
    """
    valid_json_role = json.dumps({"key": "value"})
    response = client.post(
        "/enumerator",
        json={"role": valid_json_role}
    )
    assert response.status_code == 422
    error_detail = response.json()["detail"][0]
    assert error_detail["type"] == "missing"
    assert error_detail["loc"] == ["body", "cloud_provider"]
    assert error_detail["msg"] == "Field required"


# Test 3: Missing Role Data
def test_enumerator_api_missing_role():
    """
    Test the /enumerator API when role data is missing.
    """
    response = client.post(
        "/enumerator",
        json={"cloud_provider": "AWS"}
    )
    assert response.status_code == 422
    error_detail = response.json()["detail"][0]
    assert error_detail["type"] == "missing"
    assert error_detail["loc"] == ["body", "role"]
    assert error_detail["msg"] == "Field required"


# Test 4: Empty Cloud Provider
def test_enumerator_api_empty_cloud_provider():
    """
    Test the /enumerator API when cloud provider is empty.
    """
    valid_json_role = json.dumps({"key": "value"})
    response = client.post(
        "/enumerator",
        json={
            "cloud_provider": "",
            "role": valid_json_role
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Cloud provider cannot be empty."


# Test 5: Invalid Role Format (Not JSON)
def test_enumerator_api_invalid_role_format():
    """
    Test the /enumerator API when role data is not a valid JSON object.
    """
    response = client.post(
        "/enumerator",
        json={
            "cloud_provider": "AWS",
            "role": "invalid_string"  # This should be rejected
        }
    )
    assert response.status_code == 422
    error_detail = response.json()["detail"][0]
    assert error_detail["type"] == "type_error.dict"
    assert "value is not a valid dict" in error_detail["msg"]


# Test 6: Empty Role JSON
def test_enumerator_api_empty_role_json():
    """
    Test the /enumerator API when role data is an empty JSON object.
    """
    response = client.post(
        "/enumerator",
        json={
            "cloud_provider": "AWS",
            "role": {}  # Empty JSON object
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Role data cannot be empty."


# Test 7: Special Characters in Cloud Provider
def test_enumerator_api_special_characters_cloud_provider():
    """
    Test the /enumerator API when cloud provider contains special characters.
    """
    valid_json_role = json.dumps({"key": "value"})
    response = client.post(
        "/enumerator",
from fastapi.testclient import TestClient
from main import app  # Replace with your FastAPI app file name
import pytest
from unittest.mock import patch
import json
from time import sleep

client = TestClient(app)

# Test 1: Successful Request with Valid Cloud Provider and Role (JSON)
def test_enumerator_api_success():
    """
    Test the /enumerator API with a valid cloud provider and JSON role data.
    """
    valid_json_role = json.dumps({"key": "value"})  # Any valid JSON structure
    response = client.post(
        "/enumerator",
        json={
            "cloud_provider": "AWS",
            "role": valid_json_role  # Role is JSON
        }
    )
    assert response.status_code == 200
    assert "response" in response.json()
    assert "hyperparameters" in response.json()


# Test 2: Missing Cloud Provider
def test_enumerator_api_missing_cloud_provider():
    """
    Test the /enumerator API when cloud provider is missing.
    """
    valid_json_role = json.dumps({"key": "value"})
    response = client.post(
        "/enumerator",
        json={"role": valid_json_role}
    )
    assert response.status_code == 422
    error_detail = response.json()["detail"][0]
    assert error_detail["type"] == "missing"
    assert error_detail["loc"] == ["body", "cloud_provider"]
    assert error_detail["msg"] == "Field required"


# Test 3: Missing Role Data
def test_enumerator_api_missing_role():
    """
    Test the /enumerator API when role data is missing.
    """
    response = client.post(
        "/enumerator",
        json={"cloud_provider": "AWS"}
    )
    assert response.status_code == 422
    error_detail = response.json()["detail"][0]
    assert error_detail["type"] == "missing"
    assert error_detail["loc"] == ["body", "role"]
    assert error_detail["msg"] == "Field required"


# Test 4: Empty Cloud Provider
def test_enumerator_api_empty_cloud_provider():
    """
    Test the /enumerator API when cloud provider is empty.
    """
    valid_json_role = json.dumps({"key": "value"})
    response = client.post(
        "/enumerator",
        json={
            "cloud_provider": "",
            "role": valid_json_role
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Cloud provider cannot be empty."


# Test 5: Invalid Role Format (Not JSON)
def test_enumerator_api_invalid_role_format():
    """
    Test the /enumerator API when role data is not a valid JSON object.
    """
    response = client.post(
        "/enumerator",
        json={
            "cloud_provider": "AWS",
            "role": "invalid_string"  # This should be rejected
        }
    )
    assert response.status_code == 422
    error_detail = response.json()["detail"][0]
    assert error_detail["type"] == "type_error.dict"
    assert "value is not a valid dict" in error_detail["msg"]


# Test 6: Empty Role JSON
def test_enumerator_api_empty_role_json():
    """
    Test the /enumerator API when role data is an empty JSON object.
    """
    response = client.post(
        "/enumerator",
        json={
            "cloud_provider": "AWS",
            "role": {}  # Empty JSON object
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Role data cannot be empty."


# Test 7: Special Characters in Cloud Provider
def test_enumerator_api_special_characters_cloud_provider():
    """
    Test the /enumerator API when cloud provider contains special characters.
    """
    valid_json_role = json.dumps({"key": "value"})
    response = client.post(
        "/enumerator",
        json={
            "cloud_provider": "@#$%^&*()",
            "role": valid_json_role
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Cloud provider contains invalid characters."


# Test 8: Concurrency Test (Multiple Requests)
@pytest.mark.asyncio
async def test_enumerator_api_concurrent_requests():
    """
    Test the /enumerator API with multiple concurrent requests.
    """
    valid_json_role = json.dumps({"key": "value"})

    async def send_request():
        response = client.post(
            "/enumerator",
            json={
                "cloud_provider": "AWS",
                "role": valid_json_role
            }
        )
        assert response.status_code == 200

    tasks = [send_request() for _ in range(10)]  # Simulate 10 concurrent requests
    await asyncio.gather(*tasks)


# Test 9: Backend Exception Handling (Mocked Failure)
@patch("main.generate_content", side_effect=Exception("Mocked exception"))
def test_enumerator_api_internal_error(mock_generate_content):
    """
    Test the /enumerator API when the backend function raises an exception.
    """
    valid_json_role = json.dumps({"key": "value"})
    response = client.post(
        "/enumerator",
        json={
            "cloud_provider": "AWS",
            "role": valid_json_role
        }
    )
    assert response.status_code == 500
    assert "IAM Enumerator API failed" in response.json()["detail"]


# Test 10: Slow Backend Response Handling
def mock_generate_content_slow(prompt):
    sleep(5)  # Simulate a slow backend response
    return "Mocked response", {"length": len(prompt)}

@patch("main.generate_content", side_effect=mock_generate_content_slow)
def test_enumerator_api_slow_response(mock_generate_content):
    """
    Test the /enumerator API with a slow backend response.
    """
    valid_json_role = json.dumps({"key": "value"})
    response = client.post(
        "/enumerator",
        json={
            "cloud_provider": "AWS",
            "role": valid_json_role
        }
    )
    assert response.status_code == 200
    assert "response" in response.json()


# Test 11: API Documentation Accessible
def test_api_docs():
    """
    Test if the FastAPI-generated documentation is accessible.
    """
    response = client.get("/docs")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]￼Enter        json={
            "cloud_provider": "@#$%^&*()",
            "role": valid_json_role
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Cloud provider contains invalid characters."


# Test 8: Concurrency Test (Multiple Requests)
@pytest.mark.asyncio
async def test_enumerator_api_concurrent_requests():
    """
    Test the /enumerator API with multiple concurrent requests.
    """
    valid_json_role = json.dumps({"key": "value"})

    async def send_request():
        response = client.post(
            "/enumerator",
            json={
                "cloud_provider": "AWS",
                "role": valid_json_role
            }
        )
        assert response.status_code == 200
asks = [send_request() for _ in range(10)]  # Simulate 10 concurrent requests
    await asyncio.gather(*tasks)


# Test 9: Backend Exception Handling (Mocked Failure)
@patch("main.generate_content", side_effect=Exception("Mocked exception"))
def test_enumerator_api_internal_error(mock_generate_content):
    """
    Test the /enumerator API when the backend function raises an exception.
    """
    valid_json_role = json.dumps({"key": "value"})
    response = client.post(
        "/enumerator",
        json={
            "cloud_provider": "AWS",
            "role": valid_json_role
        }
    )
    assert response.status_code == 500
    assert "IAM Enumerator API failed" in response.json()["detail"]


# Test 10: Slow Backend Response Handling
def mock_generate_content_slow(prompt):
    sleep(5)  # Simulate a slow backend response
