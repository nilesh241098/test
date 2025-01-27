import json
from unittest.mock import patch, MagicMock
import pytest
import streamlit as st


# Test 1: Valid JSON Input via Text Area
def test_valid_json_input():
    """
    Test case to verify that valid JSON data is accepted from the text area.
    """
    with patch("streamlit.text_area") as mock_text_area:
        # Simulate valid JSON data entered in the text area
        mock_text_area.return_value = '{"key": "value", "list": [1, 2, 3]}'

        # Simulate user input
        json_input = st.text_area("Enter JSON data:")
        assert json_input is not None

        # Validate JSON parsing
        try:
            parsed_data = json.loads(json_input)
            assert isinstance(parsed_data, dict) or isinstance(parsed_data, list)
        except json.JSONDecodeError:
            pytest.fail("Valid JSON input failed validation.")


# Test 2: Invalid JSON Input via Text Area
def test_invalid_json_input():
    """
    Test case to verify that invalid JSON data entered in the text area is caught.
import json
from unittest.mock import patch, MagicMock
import pytest
import streamlit as st


# Test 1: Valid JSON Input via Text Area
def test_valid_json_input():
    """
    Test case to verify that valid JSON data is accepted from the text area.
    """
    with patch("streamlit.text_area") as mock_text_area:
        # Simulate valid JSON data entered in the text area
        mock_text_area.return_value = '{"key": "value", "list": [1, 2, 3]}'

        # Simulate user input
        json_input = st.text_area("Enter JSON data:")
        assert json_input is not None

        # Validate JSON parsing
        try:
            parsed_data = json.loads(json_input)
            assert isinstance(parsed_data, dict) or isinstance(parsed_data, list)
        except json.JSONDecodeError:
            pytest.fail("Valid JSON input failed validation.")


# Test 2: Invalid JSON Input via Text Area
def test_invalid_json_input():
    """
    Test case to verify that invalid JSON data entered in the text area is caught.
    """
    with patch("streamlit.text_area") as mock_text_area:
        # Simulate invalid JSON data entered in the text area
        mock_text_area.return_value = "INVALID_JSON"

        # Simulate user input
        json_input = st.text_area("Enter JSON data:")
        assert json_input is not None

        # Validate JSON parsing
        with pytest.raises(json.JSONDecodeError):
            json.loads(json_input)


# Test 3: Valid JSON File Upload
@patch("streamlit.file_uploader")
def test_valid_json_file(mock_file_uploader):
    """
    Test case to verify that a valid JSON file is accepted.
    """
    # Mock the file uploader to return a valid JSON file
    mock_file_uploader.return_value = MagicMock()
    mock_file_uploader.return_value.read.return_value = b'{"key": "value", "list": [1, 2, 3]}'

    # Simulate file upload
    uploaded_file = st.file_uploader("Upload JSON file", type=["json"])
    assert uploaded_file is not None

    # Validate JSON parsing from file content
    try:
        file_content = uploaded_file.read().decode("utf-8")
        parsed_data = json.loads(file_content)
        assert isinstance(parsed_data, dict) or isinstance(parsed_data, list)
    except json.JSONDecodeError:
        pytest.fail("Valid JSON file failed validation.")


# Test 4: Invalid JSON File Upload
@patch("streamlit.file_uploader")
def test_invalid_json_file(mock_file_uploader):
    """
    Test case to verify that an invalid JSON file is caught.
    """
    # Mock the file uploader to return an invalid JSON file
    mock_file_uploader.return_value = MagicMock()
    mock_file_uploader.return_value.read.return_value = b"INVALID_JSON"

    # Simulate file upload
    uploaded_file = st.file_uploader("Upload JSON file", type=["json"])
    assert uploaded_file is not None

    # Validate JSON parsing from file content
    with pytest.raises(json.JSONDecodeError):
        file_content = uploaded_file.read().decode("utf-8")
        json.loads(file_content)


# Test 5: Non-JSON File Upload
@patch("streamlit.file_uploader")
def test_non_json_file(mock_file_uploader):
    """
    Test case to ensure that a non-JSON file (e.g., .txt) is rejected.
    """
    # Mock the file uploader to simulate uploading a non-JSON file
    mock_file_uploader.return_value = MagicMock()
    mock_file_uploader.return_value.name = "example.txt"
    mock_file_uploader.return_value.read.return_value = b"This is a text file, not JSON."

    # Simulate file upload
    uploaded_file = st.file_uploader("Upload JSON file", type=["json"])
    assert uploaded_file is not None

    # Validate file extension
    assert uploaded_file.name.endswith(".json"), "Uploaded file is not a JSON file."

    # Validate JSON parsing (should fail for non-JSON content)
    with pytest.raises(json.JSONDecodeError):
        file_content = uploaded_file.read().decode("utf-8")
        json.loads(file_content)￼Enter    """
    with patch("streamlit.text_area") as mock_text_area:
        # Simulate invalid JSON data entered in the text area
        mock_text_area.return_value = "INVALID_JSON"

        # Simulate user input
        json_input = st.text_area("Enter JSON data:")
        assert json_input is not None

        # Validate JSON parsing
        with pytest.raises(json.JSONDecodeError):
            json.loads(json_input)


# Test 3: Valid JSON File Upload
@patch("streamlit.file_uploader")
def test_valid_json_file(mock_file_uploader):
    """
    Test case to verify that a valid JSON file is accepted.
    """
    # Mock the file uploader to return a valid JSON file
    mock_file_uploader.return_value = MagicMock()
    mock_file_uploader.return_value.read.return_value = b'{"key": "value", "list": [1, 2, 3]}'

    # Simulate file upload
    uploaded_file = st.file_uploader("Upload JSON file", type=["json"])
sert uploaded_file is not None

    # Validate JSON parsing from file content
    try:
        file_content = uploaded_file.read().decode("utf-8")
        parsed_data = json.loads(file_content)
        assert isinstance(parsed_data, dict) or isinstance(parsed_data, list)
    except json.JSONDecodeError:
        pytest.fail("Valid JSON file failed validation.")


# Test 4: Invalid JSON File Upload
@patch("streamlit.file_uploader")
def test_invalid_json_file(mock_file_uploader):
    """
    Test case to verify that an invalid JSON file is caught.
    """
    # Mock the file uploader to return an invalid JSON file
    mock_file_uploader.return_value = MagicMock()
    mock_file_uploader.return_value.read.return_value = b"INVALID_JSON"

    # Simulate file upload
    uploaded_file = st.file_uploader("Upload JSON file", type=["json"])
    assert uploaded_file is not None

    # Validate JSON parsing from file content
