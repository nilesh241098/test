import pytest
import streamlit as st
from streamlit.testing.v1 import AppTest
from frontend_app import main  # Assuming your Streamlit file is named `frontend_app.py`

@pytest.fixture
def app():
    """Create a test instance of the Streamlit app."""
    return AppTest.from_function(main)

# ✅ Test 1: Ensure the app loads without errors
def test_app_loads(app):
    app.run()
    assert "Architecture Diagram Assistant" in app.html, "App title not found in HTML output"

# ✅ Test 2: Check if file uploader component is present
def test_file_uploader_exists(app):
    app.run()
    assert app.file_uploader[0], "File uploader component is missing"

# ✅ Test 3: Ensure template selection dropdown exists
def test_template_selection_exists(app):
    app.run()
    assert app.selectbox[0], "Template selection dropdown is missing"

# ✅ Test 4: Ensure analyze button is present
def test_analyze_button_exists(app):
    app.run()
    assert app.button[0], "Analyze button is missing"

# ✅ Test 5: Upload valid image and check if it's processed
def test_upload_valid_image(app):
    with open("test.png", "rb") as img_file:
        app.file_uploader[0].upload(img_file)
    app.run()
    assert "File uploaded successfully!" in app.html, "Valid image upload did not process correctly"

# ✅ Test 6: Upload invalid file format (e.g., `.txt`)
def test_upload_invalid_file(app):
    with open("test.txt", "w") as txt_file:
        txt_file.write("This is not an image.")
    with open("test.txt", "rb") as txt_file:
        app.file_uploader[0].upload(txt_file)
    app.run()
    assert "Invalid file format" in app.html, "Invalid file upload not handled correctly"

# ✅ Test 7: Ensure prompt is displayed after submission
def test_prompt_displayed(app):
    app.run()
    assert app.text_area[0], "Prompt text area is missing"

# ✅ Test 8: Ensure feedback form appears after analysis
def test_feedback_form(app):
    app.run()
    assert app.slider[0], "Feedback rating slider is missing"
    assert app.text_area[1], "Feedback comment box is missing"

# ✅ Test 9: Submit feedback successfully
def test_submit_feedback(app):
    app.run()
    app.slider[0].set_value(5)  # Set rating
    app.text_area[1].set_value("Great analysis!")  # Enter feedback
    app.button[1].click()  # Submit button
    app.run()
    assert "Feedback logged successfully!" in app.html, "Feedback submission failed"

# ✅ Test 10: Handle missing template selection
def test_missing_template_selection(app):
    with open("test.png", "rb") as img_file:
        app.file_uploader[0].upload(img_file)
    app.run()
    app.button[0].click()  # Analyze button
    assert "Please select a template" in app.html, "Missing template selection not handled properly"
