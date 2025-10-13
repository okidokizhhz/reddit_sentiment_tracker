# ~/reddit_sentiment_tracker/reddit_sentiment_tracker/src/utils.py
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

# Convert UTC timestamp to Vienna time
def to_vienna_time(utc_timestamp):
    dt = datetime.fromtimestamp(utc_timestamp, tz=timezone.utc).astimezone(ZoneInfo("Europe/Vienna"))
    return dt.strftime('%Y-%m-%d %H:%M:%S %Z')

