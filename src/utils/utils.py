# ~/reddit_sentiment_tracker/src/utils.py

from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import logging

logger = logging.getLogger("reddit_sentiment_tracker")

def to_vienna_time(utc_timestamp: float) -> str:
    """ converts UTC time to Vienna time """
    try:
        dt = datetime.fromtimestamp(utc_timestamp, tz=timezone.utc).astimezone(ZoneInfo("Europe/Vienna"))

        return dt.strftime('%Y-%m-%d %H:%M:%S %Z')

    except Exception as e:
        logger.error(f"Error converting UTC time to Viennese time: {e}", exc_info=True)
        return "Time conversion failed"
