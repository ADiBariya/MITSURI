#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import asyncio
import logging
from logging.handlers import RotatingFileHandler
import time
import sys

# Setup logging configuration
logging.basicConfig(
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    level=logging.INFO,
    handlers=[
        RotatingFileHandler(
            "logs/mitsuri.log", maxBytes=5000000, backupCount=10
        ),
        logging.StreamHandler(),
    ],
)

logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("motor").setLevel(logging.WARNING)
LOGGER = logging.getLogger("Mitsuri")

# Ensure log directory exists
if not os.path.exists("logs"):
    os.makedirs("logs")

# Fancy banner
def show_banner():
    banner = """
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║     ███╗   ███╗██╗████████╗███████╗██╗   ██╗██████╗ ██╗  ║
║     ████╗ ████║██║╚══██╔══╝██╔════╝██║   ██║██╔══██╗██║  ║
║     ██╔████╔██║██║   ██║   ███████╗██║   ██║██████╔╝██║  ║
║     ██║╚██╔╝██║██║   ██║   ╚════██║██║   ██║██╔══██╗██║  ║
║     ██║ ╚═╝ ██║██║   ██║   ███████║╚██████╔╝██║  ██║██║  ║
║     ╚═╝     ╚═╝╚═╝   ╚═╝   ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
           Advanced Telegram Bot Management System
"""
    print(banner)
    
# Check Python version
if sys.version_info[0] < 3 or sys.version_info[1] < 8:
    LOGGER.error("You MUST have a python version of at least 3.8! Multiple features depend on this. Bot quitting.")
    sys.exit(1)

# Check for environment variables
required_env = ["API_ID", "API_HASH", "BOT_TOKEN", "MONGO_DB_URI"]
missing_env = [var for var in required_env if not os.environ.get(var)]
if missing_env:
    LOGGER.error(f"Missing required environment variables: {', '.join(missing_env)}")
    sys.exit(1)

show_banner()

if __name__ == "__main__":
    from Mitsuri import initialize_app
    
    loop = asyncio.get_event_loop()
    LOGGER.info("Starting Mitsuri Bot...")
    
    try:
        loop.run_until_complete(initialize_app())
        LOGGER.info("Bot startup complete!")
        loop.run_forever()
    except KeyboardInterrupt:
        LOGGER.info("Stopping Mitsuri Bot...")
        loop.run_until_complete(asyncio.sleep(0.3))  # Small delay to ensure clean shutdown
    finally:
        loop.close()
        LOGGER.info("Mitsuri Bot stopped successfully.")
