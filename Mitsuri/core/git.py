import subprocess
import logging

logger = logging.getLogger("Mitsuri.core.git")


class GitManager:
    """
    Handles Git integration for Mitsuri Bot.
    Provides utilities for fetching commits and pulling updates.
    """

    @staticmethod
    def get_latest_commit():
        """
        Retrieve the latest commit hash and message from the Git repository.
        :return: Tuple (commit_hash, commit_message)
        """
        try:
            commit_hash = subprocess.check_output(
                ["git", "rev-parse", "HEAD"], text=True
            ).strip()
            commit_message = subprocess.check_output(
                ["git", "log", "-1", "--pretty=%B"], text=True
            ).strip()
            logger.info(f"Latest commit: {commit_hash} - {commit_message}")
            return commit_hash, commit_message
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to get latest commit: {e.output}")
            return None, None

    @staticmethod
    def pull_latest_changes():
        """
        Pull the latest changes from the Git repository.
        :return: Output of the git pull command
        """
        try:
            output = subprocess.check_output(
                ["git", "pull"], text=True, stderr=subprocess.STDOUT
            ).strip()
            logger.info("Git pull successful.")
            return output
        except subprocess.CalledProcessError as e:
            logger.error(f"Git pull failed: {e.output}")
            return None
