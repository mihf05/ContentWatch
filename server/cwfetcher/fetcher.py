import random
from datetime import datetime, timedelta

from blueprint import BasePlatformAdapter
from dataclass import VideoMetrics


class UniversalMetricsFetcher:
    def __init__(self):
        self._adapters = {}

    def register_platform(self, platform_name: str, adapter: BasePlatformAdapter):
        """Dynamically add platform adapters to the fetcher."""
        self._adapters[platform_name.lower()] = adapter

    def fetch(self, platform: str, video_id: str) -> VideoMetrics:
        """The single, agnostic entry point for fetching data."""
        adapter = self._adapters.get(platform.lower())
        if not adapter:
            raise ValueError(f"Platform '{platform}' is not supported or configured.")
        
        return adapter.fetch_video_data(video_id)
    


class CW_PlatformFetcher:
    def __init__(self):
        # A list of realistic content topics to randomly assign
        self.topics = ["Tech Review", "Cooking Tutorial", "Comedy Skit", "Daily Vlog", "Gaming Highlights"]

    def _generate_realistic_metrics(self, platform: str):
        """Generates views, likes, and comments that scale realistically based on the platform."""
        
        # 1. Base view count depends heavily on the platform's algorithm style
        if platform.lower() in ["tiktok", "youtube"]:
            views = random.randint(5_000, 2_500_000)
        else:  # X or Facebook
            views = random.randint(500, 150_000)

        # 2. Standard engagement scaling (Likes are usually 2% to 15% of views)
        like_percentage = random.uniform(0.02, 0.15)
        likes = int(views * like_percentage)

        # 3. Comment scaling (Comments are usually 1% to 10% of LIKES)
        comment_percentage = random.uniform(0.01, 0.10)
        comments = int(likes * comment_percentage)

        return views, likes, comments

    def fetch_video_data(self, platform: str, video_id: str) -> VideoMetrics:
        """Generates a fully formed, realistic VideoMetrics object."""
        
        views, likes, comments = self._generate_realistic_metrics(platform)
        
        # Generate a random timestamp within the last 30 days
        random_days_ago = random.randint(0, 30)
        random_hour = random.randint(0, 23)
        random_minute = random.randint(0, 59)
        posted_at = datetime.now() - timedelta(days=random_days_ago)
        posted_at = posted_at.replace(hour=random_hour, minute=random_minute)

        return VideoMetrics(
            platform=platform.capitalize(),
            video_id=video_id,
            posted_at=posted_at,
            duration_seconds=random.randint(15, 1200),  # Anywhere from a short to a long video
            content_label=random.choice(self.topics),
            views=views,
            likes=likes,
            comments=comments
        )