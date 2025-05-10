import logging
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from ..config import Config

logger = logging.getLogger("Mitsuri.platforms.Youtube")


class YouTubeAPI:
    """
    YouTube API Integration for Mitsuri Bot.
    Provides utilities to fetch video details, search, and more.
    """

    def __init__(self):
        self.api_key = Config.API_KEYS.get("youtube")
        if not self.api_key:
            raise ValueError("YouTube API key is missing in the configuration.")
        self.youtube = build("youtube", "v3", developerKey=self.api_key)

    def search_videos(self, query: str, max_results: int = 5):
        """
        Search for videos on YouTube.
        :param query: Search query
        :param max_results: Number of results to return
        :return: List of video details
        """
        try:
            logger.info(f"Searching YouTube for: {query}")
            request = self.youtube.search().list(
                q=query, part="snippet", type="video", maxResults=max_results
            )
            response = request.execute()
            videos = [
                {
                    "title": item["snippet"]["title"],
                    "channel": item["snippet"]["channelTitle"],
                    "video_id": item["id"]["videoId"],
                    "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                }
                for item in response.get("items", [])
            ]
            return videos
        except HttpError as e:
            logger.error(f"YouTube API error: {e}")
            return []

    def get_video_details(self, video_id: str):
        """
        Fetch details of a specific YouTube video.
        :param video_id: ID of the YouTube video
        :return: Video details dictionary
        """
        try:
            logger.info(f"Fetching details for video ID: {video_id}")
            request = self.youtube.videos().list(
                id=video_id, part="snippet,statistics,contentDetails"
            )
            response = request.execute()
            if not response["items"]:
                return None
            video = response["items"][0]
            return {
                "title": video["snippet"]["title"],
                "description": video["snippet"]["description"],
                "views": video["statistics"]["viewCount"],
                "likes": video["statistics"].get("likeCount", "N/A"),
                "duration": video["contentDetails"]["duration"],
                "channel": video["snippet"]["channelTitle"],
            }
        except HttpError as e:
            logger.error(f"YouTube API error: {e}")
            return None
