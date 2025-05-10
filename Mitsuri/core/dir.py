import os
import logging

logger = logging.getLogger("Mitsuri.core.dir")


class DirectoryManager:
    """
    Handles directory management for Mitsuri Bot.
    Ensures required folders exist and provides utilities for file cleanup.
    """

    REQUIRED_DIRS = ["downloads", "downloads/video", "downloads/images", "logs"]

    @classmethod
    def ensure_directories(cls):
        """
        Create required directories if they do not exist.
        """
        for dir_path in cls.REQUIRED_DIRS:
            try:
                os.makedirs(dir_path, exist_ok=True)
                logger.info(f"Ensured directory: {dir_path}")
            except Exception as e:
                logger.error(f"Failed to create directory {dir_path}: {e}")

    @staticmethod
    def clear_directory(path: str):
        """
        Clear all files in the specified directory.
        :param path: Path to the directory
        """
        if not os.path.isdir(path):
            logger.warning(f"Directory not found: {path}")
            return

        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    logger.info(f"Deleted file: {file_path}")
            except Exception as e:
                logger.error(f"Failed to delete file {file_path}: {e}")


# Ensure required directories are created at startup
DirectoryManager.ensure_directories()
