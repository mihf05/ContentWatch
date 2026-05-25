import os
from google import genai
from google.genai import types

from .dataclass import VideoMetrics
from .schema import CompleteAnalysisOutput




def generate_analytics_report(raw_metrics_data: list) -> CompleteAnalysisOutput:
    # Initializing client (automatically loads GEMINI_API_KEY from environment)
    client = genai.Client()

    prompt = f"""
    You are an expert Social Media Data Analyst. 
    Analyze the following raw bulk analytics metrics collected from our platform fetchers:
    
    {raw_metrics_data}
    
    Aggregate these metrics, identify core user behavioral patterns, calculate affinity scores, 
    and output a complete, fully structured analytical breakdown matching the provided schema.
    """

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=CompleteAnalysisOutput,
            temperature=0.2, # Lower temperature forces programmatic, structured mathematical precision
        ),
    )

    # Convert the guaranteed structured JSON text directly into native Pydantic instances
    return CompleteAnalysisOutput.model_validate_json(response.text)