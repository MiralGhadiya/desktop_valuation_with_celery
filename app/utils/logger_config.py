# app/utils/logger_config.py

import os
import sys
import logging
import queue
from logging.handlers import (
    RotatingFileHandler,
    QueueHandler,
    QueueListener,
)

# Detect Alembic environment
IS_ALEMBIC = (
    "alembic" in sys.argv[0].lower()
    or "alembic" in os.environ.get("PYTHONEXECUTABLE", "").lower()
)

# Logs directory
LOG_DIR = os.path.join(os.path.dirname(__file__), "../logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Create logger
logger = logging.getLogger("app_logger")
logger.setLevel(logging.DEBUG)

# Prevent duplicate handlers
logger.handlers.clear()
logger.propagate = False

# Queue setup (non-blocking logging)
log_queue = queue.Queue(-1)
queue_handler = QueueHandler(log_queue)
logger.addHandler(queue_handler)

# Formatter
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    "%Y-%m-%d %H:%M:%S",
)

handlers = []

# Console Handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
handlers.append(console_handler)

# File Handler (Disabled during Alembic)
if not IS_ALEMBIC:
    try:
        # Use size-based rotation (more stable on Windows)
        file_handler = RotatingFileHandler(
            LOG_FILE,
            maxBytes=10 * 1024 * 1024,  # 10MB per file
            backupCount=5,
            encoding="utf-8",
            delay=True,  # File opened only when first log is written
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)

    except Exception as e:
        print(f"Error setting up file handler: {e}")

# Queue Listener
listener = QueueListener(
    log_queue,
    *handlers,
    respect_handler_level=True,
)

listener.start()

app_logger = logger