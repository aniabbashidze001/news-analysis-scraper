"""
Custom logger setup utility using configuration from YAML file.

Creates a logger with both file and optional console output, supporting
log level control and formatting for debugging and monitoring purposes.
"""

import logging
import os
from src.utils.helpers import load_config


def setup_logger(name="news_logger"):
    """
        Sets up and returns a configured logger instance.

        Logging configuration is loaded from 'config/settings.yaml' and includes:
        - File logging to 'logs/{log_file}'
        - Optional console logging
        - Log level control for both file and console handlers

        Args:
            name (str): Name of the logger instance.

        Returns:
            logging.Logger: Configured logger object.
    """
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger  # Avoid duplicate handlers

    config = load_config("config/settings.yaml")
    log_level_str = config.get("logging", {}).get("level", "INFO")
    log_file = config.get("logging", {}).get("file", "project.log")
    enable_console = config.get("logging", {}).get("console", True)

    log_level = getattr(logging, log_level_str.upper(), logging.INFO)
    logger.setLevel(
        logging.DEBUG
    )

    os.makedirs("logs", exist_ok=True)

    # File Handler: logs everything down to DEBUG
    fh = logging.FileHandler(f"logs/{log_file}")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(fh)

    # Console Handler: obeys config logging level
    if enable_console:
        ch = logging.StreamHandler()
        ch.setLevel(log_level)
        ch.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(ch)

    return logger
