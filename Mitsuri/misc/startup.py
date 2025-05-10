import os
from pyrogram import Client
from ..core.logger import setup_logger

logger = setup_logger("Mitsuri.Startup")


async def load_plugins(client: Client, plugin_path: str = "Mitsuri/plugins"):
    """
    Load bot plugins dynamically at startup.
    :param client: Pyrogram client instance
    :param plugin_path: Path to the plugins directory
    """
    logger.info(f"Loading plugins from '{plugin_path}'...")
    for root, _, files in os.walk(plugin_path):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                module_name = os.path.relpath(os.path.join(root, file), ".").replace("/", ".").replace("\\", ".")[:-3]
                try:
                    __import__(module_name)
                    logger.info(f"Successfully loaded plugin: {module_name}")
                except Exception as e:
                    logger.error(f"Failed to load plugin {module_name}: {e}")


async def initialize_bot_data(client: Client):
    """
    Perform initial setup tasks for the bot.
    :param client: Pyrogram client instance
    """
    logger.info("Initializing bot data...")
    # Example: Add startup database initialization tasks here
    logger.info("Bot data initialized successfully.")


async def startup_tasks(client: Client):
    """
    Execute all startup tasks for Mitsuri Bot.
    :param client: Pyrogram client instance
    """
    logger.info("Starting up Mitsuri Bot...")
    await load_plugins(client)
    await initialize_bot_data(client)
    logger.info("Mitsuri Bot started successfully.")
