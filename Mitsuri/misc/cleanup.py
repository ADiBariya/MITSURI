import os
from ..core.logger import setup_logger

logger = setup_logger("Mitsuri.Cleanup")


def clear_temp_files(temp_dir: str = "downloads/temp"):
    """
    Clear temporary files from the specified directory.
    :param temp_dir: Path to the temporary files directory
    """
    logger.info(f"Clearing temporary files in '{temp_dir}'...")
    if not os.path.exists(temp_dir):
        logger.warning(f"Temporary directory '{temp_dir}' does not exist.")
        return

    try:
        for root, _, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
                logger.info(f"Deleted temp file: {file_path}")
        logger.info("Temporary files cleared successfully.")
    except Exception as e:
        logger.error(f"Failed to clear temporary files: {e}")


def cleanup_logs(log_dir: str = "logs", max_size_mb: int = 5):
    """
    Clean up log files if they exceed the specified size limit.
    :param log_dir: Path to the logs directory
    :param max_size_mb: Maximum allowed size of log files in MB
    """
    logger.info(f"Cleaning up log files in '{log_dir}'...")
    if not os.path.exists(log_dir):
        logger.warning(f"Log directory '{log_dir}' does not exist.")
        return

    try:
        for root, _, files in os.walk(log_dir):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.getsize(file_path) > max_size_mb * 1024 * 1024:
                    os.remove(file_path)
                    logger.info(f"Deleted oversized log file: {file_path}")
        logger.info("Log files cleaned up successfully.")
    except Exception as e:
        logger.error(f"Failed to clean up log files: {e}")


def perform_cleanup():
    """
    Execute all cleanup tasks for Mitsuri Bot.
    """
    logger.info("Performing cleanup tasks...")
    clear_temp_files()
    cleanup_logs()
    logger.info("Cleanup tasks completed.")
