import random

from .fetcher import CW_PlatformFetcher


cw_fetcher = CW_PlatformFetcher()

platforms = ["youtube", "tiktok", "facebook", "x"]
fake_database = []

# Generate 100 random video metrics
for i in range(100):
    chosen_platform = random.choice(platforms)
    fake_id = f"vid_{random.randint(100000, 999999)}"
    
    # Fetch the data
    metrics = cw_fetcher.fetch_video_data(chosen_platform, fake_id)
    fake_database.append(metrics)


