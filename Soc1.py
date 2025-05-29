def convert_to_mermaid(json_content: dict) -> str:
    lines = ["graph TD"]
    nodes = {}
    for element in json_content.get("elements", []):
        node_id = element["id"]
        label = element["label"]
        nodes[node_id] = label
        lines.append(f'{node_id}["{label}"]')
        for rel in element.get("relationships", []):
            target = rel["target"]
            edge_label = rel.get("type", "")
            arrow = f'-->|{edge_label}| ' if edge_label else '-->'
            lines.append(f"{node_id} {arrow} {target}")
    return "\n".join(lines)

@app.post("/v2/generate_mermaid_diagram", summary="Generate Mermaid diagram (v2)", description="Generates a structured Mermaid diagram based on the analysis response.", tags=["SOC Cloud Evidence Analyzer v2"])
async def generate_mermaid_diagram_v2(
    analysis_response: str = Form(..., description="JSON string of the analysis response from analyze_logs"),
    username: str = Depends(verify_passcode)
):
    try:
        template_content = read_prompt_template(DIAGRAM_TEMPLATE)
        prompt = create_prompt(template_content, analysis_response=analysis_response)

        response_schema = {
            "type": "object",
            "properties": {
                "diagram_structure": {
                    "type": "object"
                },
                "explanation": {
                    "type": "string"
                }
            },
            "required": ["diagram_structure", "explanation"]
        }

        response = generate_structured_content(prompt, response_schema)
        diagram_json = response["diagram_structure"]
        mermaid_code = convert_to_mermaid(diagram_json)

        logger.log_1lm_run(
            schema_name="soc_cloud_evidence_analyzer",
            prompt=prompt,
            model_response=response
        )

        return {
            "mermaid_diagram": mermaid_code,
            "explanation": response["explanation"]
        }

    except Exception as e:
        logger.error(f"Error in generate_mermaid_diagram_v2: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
