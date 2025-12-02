"""Logging configuration for S1NGULARITY.

Implements structured logging with Loguru for better observability.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from loguru import logger

# Remove default logger
logger.remove()

# Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FORMAT = os.getenv("LOG_FORMAT", "json")
LOG_FILE = os.getenv("LOG_FILE", "logs/s1ngularity.log")
LOG_ROTATION = os.getenv("LOG_ROTATION", "100 MB")
LOG_RETENTION = os.getenv("LOG_RETENTION", "30 days")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# Create logs directory
Path("logs").mkdir(exist_ok=True)

# Console handler (pretty format for development)
if DEBUG or LOG_FORMAT == "pretty":
    logger.add(
        sys.stderr,
        level=LOG_LEVEL,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True,
    )
else:
    # JSON format for production (machine-readable)
    logger.add(
        sys.stderr,
        level=LOG_LEVEL,
        format="{message}",
        serialize=True,  # JSON output
    )

# File handler (always JSON for log aggregation)
logger.add(
    LOG_FILE,
    level=LOG_LEVEL,
    format="{message}",
    serialize=True,  # JSON output
    rotation=LOG_ROTATION,
    retention=LOG_RETENTION,
    compression="zip",
    enqueue=True,  # Async logging
    backtrace=True,
    diagnose=True,
)

# Context injection
logger.configure(
    extra={
        "app": "s1ngularity",
        "env": os.getenv("APP_ENV", "development"),
        "version": "1.0.0",
    }
)


# Convenience functions
def log_api_request(method: str, path: str, **kwargs):
    """Log API request."""
    logger.info(
        "API Request",
        extra={
            "type": "api_request",
            "method": method,
            "path": path,
            **kwargs
        }
    )


def log_api_response(method: str, path: str, status_code: int, duration_ms: float, **kwargs):
    """Log API response."""
    logger.info(
        "API Response",
        extra={
            "type": "api_response",
            "method": method,
            "path": path,
            "status_code": status_code,
            "duration_ms": duration_ms,
            **kwargs
        }
    )


def log_llm_call(provider: str, model: str, tokens: int, duration_ms: float, **kwargs):
    """Log LLM API call."""
    logger.info(
        "LLM Call",
        extra={
            "type": "llm_call",
            "provider": provider,
            "model": model,
            "tokens": tokens,
            "duration_ms": duration_ms,
            **kwargs
        }
    )


def log_error(error_type: str, error_message: str, **kwargs):
    """Log application error."""
    logger.error(
        error_message,
        extra={
            "type": "application_error",
            "error_type": error_type,
            **kwargs
        }
    )


def log_feedback(session_id: str, feedback_type: str, severity: str, **kwargs):
    """Log user feedback."""
    logger.warning(
        "User Feedback",
        extra={
            "type": "user_feedback",
            "session_id": session_id,
            "feedback_type": feedback_type,
            "severity": severity,
            **kwargs
        }
    )


# Export logger
__all__ = [
    "logger",
    "log_api_request",
    "log_api_response",
    "log_llm_call",
    "log_error",
    "log_feedback",
]
