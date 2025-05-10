import logging
import tweepy
from ..config import Config

logger = logging.getLogger("Mitsuri.platforms.Twitter")


class TwitterAPI:
    """
    Twitter API Integration for Mitsuri Bot.
    Fetch tweets, profiles, and trends from Twitter.
    """

    def __init__(self):
        self.api_key = Config.API_KEYS.get("twitter")
        self.api_secret = Config.API_KEYS.get("twitter_secret")
        self.access_token = Config.API_KEYS.get("twitter_access_token")
        self.access_token_secret = Config.API_KEYS.get("twitter_access_token_secret")

        if not all([self.api_key, self.api_secret, self.access_token, self.access_token_secret]):
            raise ValueError("Twitter API credentials are missing in the configuration.")

        self.auth = tweepy.OAuthHandler(self.api_key, self.api_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)
        self.client = tweepy.API(self.auth)

    def get_user_profile(self, username: str):
        """
        Fetch Twitter user profile information.
        :param username: Twitter username
        :return: Profile details dictionary
        """
        try:
            logger.info(f"Fetching profile details for Twitter user: {username}")
            user = self.client.get_user(screen_name=username)
            return {
                "id": user.id,
                "name": user.name,
                "username": user.screen_name,
                "followers": user.followers_count,
                "following": user.friends_count,
                "tweets": user.statuses_count,
                "profile_image": user.profile_image_url_https,
            }
        except tweepy.TweepError as e:
            logger.error(f"Twitter API error: {e}")
            return None

    def get_user_tweets(self, username: str, count: int = 5):
        """
        Fetch recent tweets for a given user.
        :param username: Twitter username
        :param count: Number of tweets to fetch
        :return: List of tweets
        """
        try:
            logger.info(f"Fetching tweets for Twitter user: {username}")
            tweets = self.client.user_timeline(screen_name=username, count=count, tweet_mode="extended")
            return [
                {
                    "text": tweet.full_text,
                    "created_at": tweet.created_at,
                    "likes": tweet.favorite_count,
                    "retweets": tweet.retweet_count,
                }
                for tweet in tweets
            ]
        except tweepy.TweepError as e:
            logger.error(f"Twitter API error: {e}")
            return []
