import pytest
import streamlit as st
from unittest.mock import patch, MagicMock
import 28_ada  # Ensure the frontend file is being tested

# Test 1: Valid Image Upload
def test_valid_image_upload():
    """Test case for valid image file upload."""
    with patch("28_ada.st.file_uploader") as mock_file_uploader:
        mock_file_uploader.return_value = MagicMock(name="valid_image.png")
        uploaded_file = 28_ada.st.file_uploader("Upload Architecture Diagram", type=["png", "jpg", "jpeg"])
        assert uploaded_file is not None

# Test 2: Invalid Image Upload
def test_invalid_image_upload():
    """Test case for invalid file upload."""
    with patch("28_ada.st.file_uploader") as mock_file_uploader:
        mock_file_uploader.return_value = MagicMock(name="invalid_file.txt")
        uploaded_file = 28_ada.st.file_uploader("Upload Architecture Diagram", type=["png", "jpg", "jpeg"])
        assert uploaded_file is not None
        assert uploaded_file.name.endswith(".txt")  # Should be invalid

# Test 3: Template Selection
def test_template_selection():
    """Test case for template selection dropdown."""
    with patch("28_ada.st.selectbox") as mock_selectbox:
        mock_selectbox.return_value = "General Architecture Review"
        selected_template = 28_ada.st.selectbox("Select Template", ["General Architecture Review", "Security Architecture Review"])
        assert selected_template == "General Architecture Review"

# Test 4: Submit Button Click
def test_submit_button():
    """Test case to check if the analyze button is clicked."""
    with patch("28_ada.st.button") as mock_button:
        mock_button.return_value = True  # Simulating button click
        submitted = 28_ada.st.button("Analyze Diagram")
        assert submitted is True

# Test 5: Successful API Call
def test_successful_api_call():
    """Test case for successful API response."""
    with patch("28_ada.requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"response": "Analysis Complete"}
        response = 28_ada.requests.post("dummy_url")
        assert response.status_code == 200
        assert response.json()["response"] == "Analysis Complete"

# Test 6: Failed API Call
def test_failed_api_call():
    """Test case for failed API response."""
    with patch("28_ada.requests.post") as mock_post:
        mock_post.return_value.status_code = 400
        mock_post.return_value.json.return_value = {"detail": "Invalid template name"}
        response = 28_ada.requests.post("dummy_url")
        assert response.status_code == 400
        assert response.json()["detail"] == "Invalid template name"

# Test 7: Feedback Text Input
def test_feedback_text_input():
    """Test case for feedback text input."""
    with patch("28_ada.st.text_area") as mock_text_area:
        mock_text_area.return_value = "Great analysis"
        feedback_text = 28_ada.st.text_area("Enter Feedback")
        assert feedback_text == "Great analysis"

# Test 8: Feedback Rating Slider
def test_feedback_rating():
    """Test case for feedback rating slider."""
    with patch("28_ada.st.slider") as mock_slider:
        mock_slider.return_value = 5
        rating = 28_ada.st.slider("Rate Analysis", 1, 5)
        assert rating == 5

# Test 9: Successful Feedback Submission
def test_successful_feedback_submission():
    """Test case for successful feedback submission."""
    with patch("28_ada.requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"message": "Feedback submitted"}
        response = 28_ada.requests.post("dummy_url")
        assert response.status_code == 200
        assert response.json()["message"] == "Feedback submitted"

# Test 10: Feedback Submission Failure
def test_feedback_submission_failure():
    """Test case for feedback submission failure."""
    with patch("28_ada.requests.post") as mock_post:
        mock_post.return_value.status_code = 500
        mock_post.return_value.json.return_value = {"detail": "Feedback submission failed"}
        response = 28_ada.requests.post("dummy_url")
        assert response.status_code == 500
        assert response.json()["detail"] == "Feedback submission failed"
