# ~/reddit_sentiment_tracker/src/logger.py

import logging
import sys
from logging.handlers import RotatingFileHandler
from .config import LOG_DIR
from pathlib import Path

def setup_logger(name: str ="reddit_sentiment_tracker", level: int = logging.INFO) -> logging.Logger:
    """
    Setup logger with both console and file handlers
    """
    
    logger = logging.getLogger(name)  # MOVE THIS UP - define logger FIRST

    # avoid duplicate handlers
    if logger.handlers:
        return logger

    # set logger level
    logger.setLevel(level)

    # formatter
    detailed_formatter = logging.Formatter(
        fmt="%(asctime)s | %(name)s | %(levelname)-8s | %(funcName)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
 
    console_formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%H:%M:%S"
    )

    # Console handler - Info and above
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    
    # File handler with rotation - Debug and above
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        log_file = LOG_DIR / f"{name}.log"
        error_log_file = LOG_DIR / f"{name}.errors.log"
    except PermissionError:
        # Fallback for Hugging Face Spaces
        fallback_log_dir = Path("/tmp/logs")
        fallback_log_dir.mkdir(parents=True, exist_ok=True)
        log_file = fallback_log_dir / f"{name}.log"
        error_log_file = fallback_log_dir / f"{name}.errors.log"
    
    file_handler = RotatingFileHandler(
        filename=str(log_file),
        maxBytes=5_000_000,  # 5MB
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)

    # Error file handler - ERROR and above only
    error_handler = RotatingFileHandler(
        filename=str(error_log_file),
        maxBytes=5_000_000,  # 5MB
        backupCount=5,  # 5 Backups
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed_formatter)

    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(error_handler)

    # Prevent propagation to root logger
    logger.propagate = False

    logger.info(f"Logger '{name}' initialized - Log files: {log_file}")
    return logger
