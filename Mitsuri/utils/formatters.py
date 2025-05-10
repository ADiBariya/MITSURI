from datetime import datetime, timedelta


def format_time(seconds: int) -> str:
    """
    Format seconds into a human-readable time string.
    :param seconds: Time in seconds
    :return: Formatted time string (e.g., "1h 30m 45s")
    """
    delta = timedelta(seconds=seconds)
    days, remainder = divmod(delta.total_seconds(), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    time_string = []
    if days:
        time_string.append(f"{int(days)}d")
    if hours:
        time_string.append(f"{int(hours)}h")
    if minutes:
        time_string.append(f"{int(minutes)}m")
    if seconds:
        time_string.append(f"{int(seconds)}s")

    return " ".join(time_string)


def format_date(timestamp: int) -> str:
    """
    Convert a UNIX timestamp to a human-readable date.
    :param timestamp: UNIX timestamp
    :return: Formatted date (e.g., "2025-05-10")
    """
    return datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")


def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to a specific length with ellipsis if needed.
    :param text: Original text
    :param max_length: Maximum length of the text
    :return: Truncated text
    """
    return text if len(text) <= max_length else f"{text[:max_length]}..."
