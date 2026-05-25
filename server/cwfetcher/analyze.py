import os
from google import genai
from google.genai import types

from .dataclass import VideoMetrics


def analyze_video_with_gemini(video_data: VideoMetrics) -> VideoAnalysis:
    # Initialize the standard GenAI client (picks up GEMINI_API_KEY from environment)
    client = genai.Client()

    # Construct a prompt combining the metrics and context
    prompt = f"""
    Analyze the following video performance data from {video_data.platform}:
    - Video ID: {video_data.video_id}
    - Content Label/Title Hint: {video_data.content_label}
    - Duration: {video_data.duration_seconds} seconds
    - Views: {video_data.views:,}
    - Likes: {video_data.likes:,}
    - Comments: {video_data.comments:,}
    - Calculated Engagement Rate: {video_data.engagement_rate:.2f}%
    """

    # Call the Gemini model
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            # This forces the model to return JSON matching our Pydantic schema
            response_mime_type="application/json",
            response_schema=VideoAnalysis,
            temperature=0.2, # Low temperature for more analytical/consistent responses
        ),
    )

    # The response.text is guaranteed to be valid JSON matching VideoAnalysis
    # We use Pydantic to parse it back into a clean Python object
    return VideoAnalysis.model_validate_json(response.text)