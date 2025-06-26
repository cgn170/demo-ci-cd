from pydantic import BaseModel

from logging.config import dictConfig
import logging


def get_logger(settings=None, logger_name='demo'):
    """
    Retrieves a logger instance with the specified name.

    This function returns a logger object, which can be used to log messages
    throughout the application. If no settings are provided, it defaults to
    using the application's default logger configuration.

    Args:
        settings (dict, optional): Configuration settings for the logger. 
            If None, the default logger configuration will be used.
        logger_name (str, optional): The name of the logger to retrieve. 
            Defaults to 'demo'.

    Returns:
        logging.Logger: A configured logger instance.
    """
    # If settings are provided, configure the logger accordingly.
    # Otherwise, fallback to the default logger configuration.

    return get_default_logger(logger_name)


def get_default_logger(logger_name: str):
    """
    Retrieves a logger instance with the specified name, configured using the default logging configuration.

    This function initializes the logging system using a predefined configuration
    and returns a logger object that can be used to log messages.

    Args:
        logger_name (str): The name of the logger to retrieve.

    Returns:
        logging.Logger: A logger instance configured with the default settings.

    Note:
        Ensure that the `LogConfig` class and its `dict` method are properly defined
        and imported before using this function. The `dictConfig` function is used
        to apply the logging configuration.
    """

    dictConfig(LogConfig().dict())
    return logging.getLogger(logger_name)


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "demo"
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers = {
        "demo": {"handlers": ["default"], "level": LOG_LEVEL},
    }
