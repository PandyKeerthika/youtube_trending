# fetch_youtube_data.py

import requests
import pandas as pd
import os

# Replace with your actual API Key or use environment variable later
API_KEY = "AIzaSyBAE3UHyS2mF51SYJlMDjDktivMxPAhDPU"
REGION_CODE = "US"
MAX_RESULTS = 20

url = (
    f"https://www.googleapis.com/youtube/v3/videos"
    f"?part=snippet,statistics&chart=mostPopular"
    f"&regionCode={REGION_CODE}&maxResults={MAX_RESULTS}&key={API_KEY}"
)

response = requests.get(url)
data = response.json()

videos = []
for item in data["items"]:
    video = {
        "video_id": item["id"],
        "title": item["snippet"]["title"],
        "channel": item["snippet"]["channelTitle"],
        "views": int(item["statistics"].get("viewCount", 0)),
        "likes": int(item["statistics"].get("likeCount", 0)),
        "published_at": item["snippet"]["publishedAt"]
    }
    videos.append(video)

df = pd.DataFrame(videos)
df.to_csv("realtime_trending.csv", index=False)

print("✅ Saved trending videos to realtime_trending.csv")
