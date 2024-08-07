import logging
import os
from enum import Enum
from pathlib import Path

from qgis.core import (
    Qgis,
    QgsApplication,
    QgsMessageLog,
)

from plugin.utilities.resources import (
    get_env_variable,
    get_plugin_name,
)


class LogLevel(Enum):
    NOTSET = logging.NOTSET
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARN = logging.WARN
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class QgisLogHandler(logging.Handler):
    """Log handler emitting log event to QgsMessageLog"""

    def __init__(self, level: int = logging.NOTSET) -> None:
        logging.Handler.__init__(self, level=level)

    def emit(self, record: logging.LogRecord) -> None:
        if record.levelno in (logging.ERROR, logging.CRITICAL):
            qgis_level = Qgis.MessageLevel.Critical
        elif record.levelno == logging.WARNING:
            qgis_level = Qgis.MessageLevel.Warning
        else:
            qgis_level = Qgis.MessageLevel.Info

        QgsMessageLog.logMessage(
            self.format(record), get_plugin_name(), qgis_level
        )


def get_qgis_log_handler(log_level: int) -> QgisLogHandler:
    """Get log handler for QGIS user logging. These log messages are shown
    to the users. Logs are shown in Log Messages Panel

    Args:
        log_level (int): logging level for handler

    Returns:
        QgisLogHandler: QgisLogHandler class
    """
    qgis_message_log_handler = QgisLogHandler()
    qgis_message_log_handler.setLevel(log_level)
    qgis_message_log_format = logging.Formatter(
        "%(filename)s:%(funcName)s():%(lineno)d - %(message)s"
    )
    qgis_message_log_handler.setFormatter(qgis_message_log_format)

    return qgis_message_log_handler


def get_file_log_handler(log_level: int) -> logging.FileHandler:
    """Get log handler for file logging. This is used for debugging purposes

    Args:
        log_level (int): logging level for handler

    Returns:
        logging.FileHandler: FileHandler class
    """
    log_path = (
        Path(QgsApplication.qgisSettingsDirPath()) / f"{get_plugin_name()}.log"
    )

    file_handler = logging.FileHandler(str(log_path))
    file_handler.setLevel(log_level)
    file_log_format = logging.Formatter(
        "%(asctime)s - [%(levelname)s] - %(filename)s:%(funcName)s():%(lineno)d - %(message)s",  # noqa: E501
        "%d.%m.%Y %H:%M:%S",
    )
    file_handler.setFormatter(file_log_format)

    return file_handler


def get_implicit_log_level() -> int:
    """Get implicit logging level

    Returns:
        int: logging level
    """
    if get_env_variable("PLUGIN_DEBUGGING_ENABLED") == "1":
        return logging.DEBUG

    return logging.INFO


def get_logging_level() -> int:
    """Set logging level from environment variable.
    Otherwise default to implicit log level

    https://docs.python.org/3/library/logging.html#levels

    Returns:
        int: logging level
    """
    log_level = os.environ.get("PLUGIN_LOG_LEVEL")
    if log_level is None:
        return get_implicit_log_level()

    try:
        return int(log_level)
    except (TypeError, ValueError):
        return get_implicit_log_level()


def get_plugin_logger() -> logging.Logger:
    """Return plugin logger

    Returns:
        logging.Logger: plugin logger instance
    """
    return logging.getLogger(get_plugin_name())


def init_logger(logger_name: str) -> None:
    """Initialize logger and its handlers

    Args:
        logger_name (str): name for the custom logger
    """
    logger = logging.getLogger(logger_name)

    log_level = get_logging_level()
    logger.setLevel(log_level)

    logger.addHandler(get_qgis_log_handler(log_level))

    if get_env_variable("DEBUGGING_ENABLED") == "1":
        logger.addHandler(get_file_log_handler(log_level))


def remove_logger(logger_name: str) -> None:
    """Remove custom logger with provided name

    Args:
        logger_name (str): logger name to remove
    """
    logger = logging.getLogger(logger_name)

    for handler in logger.handlers[:]:
        if isinstance(handler, logging.FileHandler):
            handler.close()

        logger.removeHandler(handler)
