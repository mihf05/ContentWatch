from abc import ABC, abstractmethod

from dataclass import VideoMetrics

class BasePlatformAdapter(ABC):
    
    @abstractmethod
    def authenticate(self) -> None:
        """Handle API keys, OAuth, or session tokens."""
        pass

    @abstractmethod
    def fetch_video_data(self, video_id: str) -> VideoMetrics:
        """Fetch raw data from the platform and return the standardized VideoMetrics."""
        pass