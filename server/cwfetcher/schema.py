from pydantic import BaseModel, Field

class GeminiInsightSchema(BaseModel):
    best_content_type: str = Field(description="The format that performed best, e.g., 'Short-form video', 'Carousel'")
    best_topic: str = Field(description="The highest engaging topic, e.g., 'Python Tech', 'Cooking Tips'")
    best_posting_time: str = Field(description="Optimal bucket time, e.g., 'morning', 'evening'")
    best_duration: str = Field(description="Optimal video length bucket, e.g., '15-30s', '5-10m'")
    strategy: str = Field(description="A detailed paragraphs outlining actionable next steps for the user.")
    confidence_score: float = Field(description="Confidence rating of this data insight between 0.0 and 1.0")

class GeminiContentDNASchema(BaseModel):
    short_form_affinity: float = Field(description="Affinity score for short videos vs long videos from 0.0 to 1.0")
    education_score: float = Field(description="Calculated education value index from 0.0 to 1.0")
    entertainment_score: float = Field(description="Calculated entertainment value index from 0.0 to 1.0")
    
    morning_performance: float = Field(description="Normalized weight performance score for morning postings (0.0 to 1.0)")
    evening_performance: float = Field(description="Normalized weight performance score for evening postings (0.0 to 1.0)")
    night_performance: float = Field(description="Normalized weight performance score for night postings (0.0 to 1.0)")

# A master schema container so Gemini can generate both models in a single API call
class CompleteAnalysisOutput(BaseModel):
    insight: GeminiInsightSchema
    content_dna: GeminiContentDNASchema