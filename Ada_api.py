from fastapi import FastAPI, File, UploadFile, Form, HTTPException from fastapi.responses import JSONResponse from PIL import Image as PILImage import io import logging

app = FastAPI()

Constants

EXPERIMENT_NAME = "architecture_diagram_assistant" TEMPLATE_PATHS = { "General Architecture Review": "prompts/ada/general_architecture", "Security Architecture Review": "prompts/ada/security_architecture", "Infrastructure Architecture Review": "prompts/ada/infrastructure_architecture", "Application Architecture Review": "prompts/ada/application_architecture", "Cloud Architecture Review": "prompts/ada/cloud_architecture", } MAX_WIDTH = 3840 MAX_HEIGHT = 2400

Functions (assume they are defined elsewhere in your project)

- resize_image_if_needed(image_data)

- enhance_image(image_data)

- create_prompt(template_content)

- generate_content_stream(prompt, image)

- read_prompt_template(template_path)

@app.post("/analyze_diagram") async def analyze_diagram(file: UploadFile = File(...), template_name: str = Form(...)): if template_name not in TEMPLATE_PATHS: raise HTTPException(status_code=400, detail="Invalid template selected")

template_path = TEMPLATE_PATHS[template_name]
template_content = read_prompt_template(template_path)
if not template_content:
    raise HTTPException(status_code=400, detail="Template content could not be loaded")

try:
    image_data = await file.read()
    resized_image_data, new_size = resize_image_if_needed(image_data)
    original_size = PILImage.open(io.BytesIO(image_data)).size

    if new_size != original_size:
        logging.info(f"Image was resized from {original_size} to {new_size} to fit within {MAX_WIDTH}x{MAX_HEIGHT}")
    
    enhanced_image = enhance_image(resized_image_data)
    prompt = create_prompt(template_content)
    response = generate_content_stream(prompt, enhanced_image)
    
    return JSONResponse(content={"prompt": prompt, "response": response})
except Exception as e:
    logging.error(f"An error occurred: {e}")
    raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
