#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from typing import List, Set, Dict, Any, Optional
import json
from dotenv import load_dotenv
import logging

# Load .env file
load_dotenv()

logger = logging.getLogger("Mitsuri.config")

class Config:
    """Configuration for Mitsuri Bot"""
    
    # Core API Config
    API_ID: int = int(os.environ.get("API_ID", 0))
    API_HASH: str = os.environ.get("API_HASH", "")
    BOT_TOKEN: str = os.environ.get("BOT_TOKEN", "")
    
    # MongoDB
    MONGO_DB_URI: str = os.environ.get("MONGO_DB_URI", "")
    
    # Bot Owner & Sudo Users
    OWNER_ID: int = int(os.environ.get("OWNER_ID", 0))
    SUDO_USERS: List[int] = [
        int(x) for x in os.environ.get("SUDO_USERS", "").split()
        if x.isdigit()
    ]
    if OWNER_ID not in SUDO_USERS:
        SUDO_USERS.append(OWNER_ID)
    
    # Channels & Groups
    LOG_CHANNEL_ID: Optional[int] = int(os.environ.get("LOG_CHANNEL_ID", 0)) or None
    SUPPORT_GROUP: Optional[str] = os.environ.get("SUPPORT_GROUP")
    UPDATES_CHANNEL: Optional[str] = os.environ.get("UPDATES_CHANNEL")
    
    # Bot Customization
    BOT_NAME: str = os.environ.get("BOT_NAME", "Mitsuri")
    BOT_USERNAME: Optional[str] = os.environ.get("BOT_USERNAME")
    
    # Media Settings
    MAX_DOWNLOAD_SIZE: int = int(os.environ.get("MAX_DOWNLOAD_SIZE", 100)) * 1024 * 1024  # in bytes
    MAX_VIDEO_DURATION: int = int(os.environ.get("MAX_VIDEO_DURATION", 10)) * 60  # in seconds
    DOWNLOAD_TIMEOUT: int = int(os.environ.get("DOWNLOAD_TIMEOUT", 300))  # in seconds
    
    # Plugin Settings
    DISABLED_PLUGINS: List[str] = os.environ.get("DISABLED_PLUGINS", "").split()
    
    # Admin Settings
    DELETE_COMMANDS: bool = os.environ.get("DELETE_COMMANDS", "False").lower() == "true"
    COMMAND_PREFIXES: List[str] = list(os.environ.get("COMMAND_PREFIXES", "! / .").split())
    
    # Rate Limiting
    RATE_LIMIT: int = int(os.environ.get("RATE_LIMIT", 3))  # messages per second
    RATE_LIMIT_WINDOW: int = int(os.environ.get("RATE_LIMIT_WINDOW", 5))  # in seconds
    
    # Blacklisted Words and Users
    BLACKLISTED_WORDS: List[str] = []
    BLACKLISTED_USERS: List[int] = []
    
    # Auto-generated list of commands (will be populated during startup)
    ALL_COMMANDS: Dict[str, str] = {}
    
    # Webhook (if needed)
    WEBHOOK_URL: Optional[str] = os.environ.get("WEBHOOK_URL")
    WEBHOOK_PORT: int = int(os.environ.get("WEBHOOK_PORT", 8443))
    
    # Git Update Settings
    ENABLE_GIT_UPDATER: bool = os.environ.get("ENABLE_GIT_UPDATER", "False").lower() == "true"
    GIT_REPO_URL: Optional[str] = os.environ.get("GIT_REPO_URL")
    GIT_BRANCH: str = os.environ.get("GIT_BRANCH", "main")
    
    # Platform API Keys
    YOUTUBE_API_KEY: Optional[str] = os.environ.get("YOUTUBE_API_KEY")
    TWITTER_API_KEY: Optional[str] = os.environ.get("TWITTER_API_KEY")
    TWITTER_API_SECRET: Optional[str] = os.environ.get("TWITTER_API_SECRET")
    TWITTER_ACCESS_TOKEN: Optional[str] = os.environ.get("TWITTER_ACCESS_TOKEN")
    TWITTER_ACCESS_SECRET: Optional[str] = os.environ.get("TWITTER_ACCESS_SECRET")
    INSTAGRAM_USERNAME: Optional[str] = os.environ.get("INSTAGRAM_USERNAME")
    INSTAGRAM_PASSWORD: Optional[str] = os.environ.get("INSTAGRAM_PASSWORD")

    @classmethod
    def load_blacklists(cls) -> None:
        """Load blacklisted words and users from files if they exist"""
        try:
            if os.path.exists("./data/blacklisted_words.json"):
                with open("./data/blacklisted_words.json", "r") as f:
                    cls.BLACKLISTED_WORDS = json.load(f)
                    
            if os.path.exists("./data/blacklisted_users.json"):
                with open("./data/blacklisted_users.json", "r") as f:
                    cls.BLACKLISTED_USERS = json.load(f)
        except Exception as e:
            logger.error(f"Error loading blacklists: {str(e)}")
    
    @classmethod
    def update_blacklisted_words(cls, words: List[str]) -> None:
        """Update blacklisted words and save to file"""
        cls.BLACKLISTED_WORDS = words
        os.makedirs("./data", exist_ok=True)
        with open("./data/blacklisted_words.json", "w") as f:
            json.dump(words, f)
    
    @classmethod
    def update_blacklisted_users(cls, users: List[int]) -> None:
        """Update blacklisted users and save to file"""
        cls.BLACKLISTED_USERS = users
        os.makedirs("./data", exist_ok=True)
        with open("./data/blacklisted_users.json", "w") as f:
            json.dump(users, f)
    
    @classmethod
    def register_command(cls, command: str, description: str) -> None:
        """Register a command and its description"""
        cls.ALL_COMMANDS[command] = description

# Load blacklists at startup
Config.load_blacklists()
