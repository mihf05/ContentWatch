from datetime import datetime
from typing import Optional
from dataclasses import dataclass

@dataclass
class VideoMetrics:
    # Metadata
    platform: str
    video_id: str
    posted_at: datetime
    duration_seconds: int
    content_label: str  # e.g., "Tutorial", "Comedy", "Tech"
    
    # Raw Metrics
    views: int
    likes: int
    comments: int
    
    # Derived Features (Calculated automatically on initialization)
    @property
    def like_ratio(self) -> float:
        return self.likes / self.views if self.views > 0 else 0.0

    @property
    def comment_ratio(self) -> float:
        return self.comments / self.views if self.views > 0 else 0.0

    @property
    def engagement_rate(self) -> float:
        # Standard industry formula: (Engagements / Views) * 100
        total_interactions = self.likes + self.comments
        return (total_interactions / self.views) * 100 if self.views > 0 else 0.0

    @property
    def time_bucket(self) -> str:
        hour = self.posted_at.hour
        if 5 <= hour < 12:
            return "morning"
        elif 12 <= hour < 17:
            return "afternoon"
        elif 17 <= hour < 22:
            return "evening"
        else:
            return "night"