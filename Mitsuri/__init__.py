#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Mitsuri - Advanced Telegram Bot
Using Pyrogram and MongoDB
"""

import asyncio
import logging
import time
from datetime import datetime
from typing import Optional, Dict, Any, List
import os

# Core Modules
from .core.bot import MitsuriBot
from .core.mongo import MongoDB
from .core.dir import setup_directories
from .core.git import GitManager

# Utils
from .utils.helpers import load_modules
from .misc.startup import run_startup_tasks

# Set up logger
logger = logging.getLogger("Mitsuri")

# Load configuration
from .config import Config

# Initialize MongoDB connection
db: Optional[MongoDB] = None
# Initialize bot instance
bot: Optional[MitsuriBot] = None
# Start time
START_TIME = time.time()

class MitsuriContext:
    """Context class to store application state and provide access to core components"""
    def __init__(self):
        self.db = None
        self.bot = None
        self.start_time = START_TIME
        self.git = None
        
        # Bot statistics
        self.stats = {
            "messages_processed": 0,
            "commands_executed": 0,
            "users_total": 0,
            "groups_total": 0,
        }
        
    @property
    def uptime(self) -> str:
        """Returns formatted uptime string"""
        uptime_seconds = int(time.time() - self.start_time)
        hours, remainder = divmod(uptime_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        
        if days > 0:
            return f"{days}d {hours}h {minutes}m {seconds}s"
        else:
            return f"{hours}h {minutes}m {seconds}s"
    
    def increment_stat(self, stat_name: str, increment: int = 1) -> None:
        """Increment a statistics counter"""
        if stat_name in self.stats:
            self.stats[stat_name] += increment

# Create global context
ctx = MitsuriContext()

async def initialize_app() -> None:
    """Initialize the Mitsuri application"""
    global db, bot, ctx
    
    try:
        # Setup directories
        logger.info("Mitsuri.core.dir - Setting up directories...")
        setup_directories()
        logger.info("Mitsuri.core.dir - Directories Updated.")
        
        # Initialize MongoDB
        logger.info("Mitsuri.core.mongo - Connecting to your Mongo Database...")
        db = MongoDB(Config.MONGO_DB_URI)
        await db.initialize()
        ctx.db = db
        logger.info("Mitsuri.core.mongo - Connected to your Mongo Database.")
        
        # Initialize Git manager if needed
        if Config.ENABLE_GIT_UPDATER:
            logger.info("Mitsuri.core.git - Initializing Git manager...")
            ctx.git = GitManager()
            if ctx.git.is_repo():
                logger.info("Mitsuri.core.git - Git Client Found [VPS DEPLOYER]")
            else:
                logger.warning("Mitsuri.core.git - No Git repository found.")
        
        # Load database essentials
        logger.info("Mitsuri.misc - Loading database essentials...")
        await run_startup_tasks(db)
        logger.info("Mitsuri.misc - Database loaded ......")
        
        # Initialize the bot
        logger.info("Mitsuri.core.bot - Mitsuri Starting...")
        bot = MitsuriBot(
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            mongodb=db,
            context=ctx
        )
        ctx.bot = bot
        
        # Load plugins
        load_modules(bot)
        
        # Start the bot
        await bot.start()
        logger.info(f"Mitsuri.core.bot - Bot started successfully as @{bot.me.username}")
        
        # Set bot commands
        await bot.set_bot_commands([
            ("start", "Start the bot"),
            ("help", "Get help with bot commands"),
            ("settings", "Adjust your personal settings"),
            ("about", "About this bot"),
            ("ping", "Check bot's ping"),
        ])
        
        # Schedule periodic tasks
        bot.loop.create_task(periodic_tasks())
        
    except Exception as e:
        logger.error(f"Error during initialization: {str(e)}", exc_info=True)
        raise

async def periodic_tasks():
    """Periodic tasks to run in the background"""
    while True:
        try:
            # Update stats in DB every 5 minutes
            await db.update_stats(ctx.stats)
            
            # Clean up expired data
            await db.cleanup_expired_data()
            
            # Wait for next interval
            await asyncio.sleep(300)  # 5 minutes
        except Exception as e:
            logger.error(f"Error in periodic tasks: {str(e)}")
            await asyncio.sleep(60)  # Retry after 1 minute on error
