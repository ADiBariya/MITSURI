import logging
import requests
from ..config import Config

logger = logging.getLogger("Mitsuri.platforms.Instagram")


class InstagramAPI:
    """
    Instagram API Integration for Mitsuri Bot.
    Fetch profile details, posts, and media from Instagram.
    """

    BASE_URL = "https://graph.instagram.com"

    def __init__(self):
        self.access_token = Config.API_KEYS.get("instagram")
        if not self.access_token:
            raise ValueError("Instagram API access token is missing in the configuration.")

    def get_user_profile(self, user_id: str):
        """
        Fetch Instagram user profile information.
        :param user_id: Instagram user ID
        :return: Profile details dictionary
        """
        url = f"{self.BASE_URL}/{user_id}?fields=id,username,account_type,media_count&access_token={self.access_token}"
        try:
            logger.info(f"Fetching profile details for user ID: {user_id}")
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Instagram API error: {e}")
            return None

    def get_user_media(self, user_id: str, limit: int = 5):
        """
        Fetch recent media for a given Instagram user.
        :param user_id: Instagram user ID
        :param limit: Number of media items to fetch
        :return: List of media details
        """
        url = f"{self.BASE_URL}/{user_id}/media?fields=id,caption,media_type,media_url,thumbnail_url,timestamp&limit={limit}&access_token={self.access_token}"
        try:
            logger.info(f"Fetching media for user ID: {user_id}")
            response = requests.get(url)
            response.raise_for_status()
            return response.json().get("data", [])
        except requests.RequestException as e:
            logger.error(f"Instagram API error: {e}")
            return []
