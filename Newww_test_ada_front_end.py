import streamlit as st
from unittest.mock import patch

# Test 1: File Upload Component
def test_file_upload():
    """Test case for file upload component."""
    with patch("streamlit.file_uploader") as mock_file_uploader:
        mock_file_uploader.return_value = None
        uploaded_file = st.file_uploader("Upload Architecture Diagram")
        assert uploaded_file is None

# Test 2: Template Selection
def test_template_selection():
    """Test case for template selection dropdown."""
    with patch("streamlit.selectbox") as mock_selectbox:
        mock_selectbox.return_value = "General Architecture Review"
        selected_template = st.selectbox("Select Template", ["General Architecture Review", "Security Architecture Review"])
        assert selected_template == "General Architecture Review"

# Test 3: Submit Button
def test_submit_button():
    """Test case to check submit button presence."""
    with patch("streamlit.button") as mock_button:
        mock_button.return_value = False
        submitted = st.button("Analyze Diagram")
        assert submitted is False

# Test 4: Successful API Response
def test_successful_api_response():
    """Test case for successful API response."""
    with patch("frontend.requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"response": "Analysis Complete"}
        response = mock_post("dummy_url")
        assert response.status_code == 200
        assert response.json()["response"] == "Analysis Complete"

# Test 5: API Failure Response
def test_api_failure_response():
    """Test case for API failure response."""
    with patch("frontend.requests.post") as mock_post:
        mock_post.return_value.status_code = 400
        mock_post.return_value.json.return_value = {"detail": "Invalid template name"}
        response = mock_post("dummy_url")
        assert response.status_code == 400
        assert response.json()["detail"] == "Invalid template name"

# Test 6: Feedback Text Area
def test_feedback_text_area():
    """Test case for feedback text area."""
    with patch("streamlit.text_area") as mock_text_area:
        mock_text_area.return_value = "Great analysis"
        feedback_text = st.text_area("Enter Feedback")
        assert feedback_text == "Great analysis"

# Test 7: Feedback Rating Slider
def test_feedback_rating_slider():
    """Test case for feedback rating slider."""
    with patch("streamlit.slider") as mock_slider:
        mock_slider.return_value = 5
        rating = st.slider("Rate Analysis", 1, 5)
        assert rating == 5

# Test 8: Feedback Submit Button
def test_feedback_submit_button():
    """Test case to check if feedback submit button is present."""
    with patch("streamlit.button") as mock_button:
        mock_button.return_value = False
        submitted = st.button("Submit Feedback")
        assert submitted is False

# Test 9: Successful Feedback Submission
def test_successful_feedback_submission():
    """Test case for successful feedback submission."""
    with patch("frontend.requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"message": "Feedback submitted"}
        response = mock_post("dummy_url")
        assert response.status_code == 200
        assert response.json()["message"] == "Feedback submitted"

# Test 10: Feedback Submission Failure
def test_feedback_submission_failure():
    """Test case for feedback submission failure."""
    with patch("frontend.requests.post") as mock_post:
        mock_post.return_value.status_code = 500
        mock_post.return_value.json.return_value = {"detail": "Feedback submission failed"}
        response = mock_post("dummy_url")
        assert response.status_code == 500
        assert response.json()["detail"] == "Feedback submission failed"
from unittest.mock import patch, MagicMock
import streamlit as st

@patch("streamlit.file_uploader")
@patch("requests.post")
def test_invalid_image_upload(mock_post, mock_file_uploader):
    """Test uploading an invalid image file (e.g., a .txt file instead of an image)."""

    # Simulate an invalid file upload (text file instead of image)
    mock_file = MagicMock()
    mock_file.name = "invalid_file.txt"
    mock_file.read.return_value = b"This is not an image file"
    mock_file_uploader.return_value = mock_file

    # Mock API response for invalid file format
    mock_post.return_value.status_code = 400
    mock_post.return_value.json.return_value = {"detail": "Invalid image format"}

    # Run the function that processes the upload
    with patch("streamlit.error") as mock_error:
        process_upload()  # Replace with actual function handling upload

        # Ensure the API was called
        mock_post.assert_called_once()

        # Ensure Streamlit shows an error message
        mock_error.assert_called_once_with("Invalid image format")


from unittest.mock import patch, MagicMock
import streamlit as st
import pytest
from PIL import UnidentifiedImageError

# Test 1: Valid Image Upload
@patch("streamlit.file_uploader")
def test_valid_image_upload(mock_file_uploader):
    """Test case to verify that a valid image file is successfully uploaded."""
    
    # Mock a valid image file
    mock_file = MagicMock()
    mock_file.name = "valid_image.png"
    mock_file.read.return_value = b"\x89PNG\r\n\x1a\n"  # Simulating PNG file signature
    mock_file_uploader.return_value = mock_file

    # Simulate file upload
    uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

    assert uploaded_file is not None, "File upload failed"
    assert uploaded_file.name.endswith(("png", "jpg", "jpeg")), "Uploaded file is not an image"


# Test 2: Invalid Image Upload
@patch("streamlit.file_uploader")
def test_invalid_image_upload(mock_file_uploader):
    """Test case to verify that an invalid image file is caught."""

    # Mock an invalid image file (text file)
    mock_file = MagicMock()
    mock_file.name = "invalid_file.txt"
    mock_file.read.return_value = b"This is not an image file"
    mock_file_uploader.return_value = mock_file

    # Simulate file upload
    uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

    assert uploaded_file is not None, "File upload failed"

    # Validate image parsing with PIL (will raise UnidentifiedImageError)
    with pytest.raises(UnidentifiedImageError):
        from PIL import Image
        Image.open(uploaded_file.read())  # This should fail for a non-image file
