import os
import logging
from logging.handlers import RotatingFileHandler
from typing import Optional


class Logger:
    def __init__(
        self,
        debug: bool = False,
        identifier: str = "my_celery_app",
        max_bytes: int = 10485760, #10MB
        backup_count: int = 5
    ) -> None:
        """
        Initialize the logger with rotating file handling and optional debug mode (format).
        Args:
            debug (bool): Enable detailed debug loggine if True, else use basic infor logging.
            identifier (str): Identifier name.
            max_bytes (int): Max size of log file in bytes before rotation (default: 10MB).
            backup_count (int): Number of backup log files to keep (default: 5).
        """
        self.logger: logging.Logger = logging.getLogger(identifier)
        self.logger.setLevel(logging.DEBUG if debug else logging.INFO)

        # Log directory
        log_file = f"{identifier}.log"
        log_path = os.path.join(os.getcwd(), 'LOGS')
        if not os.path.isdir(log_path):
            os.mkdir(log_path)
        
        # Configure rotating handler
        file_handler = RotatingFileHandler(
            filename=os.path.join(log_path, log_file),
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf8"
        )
        file_handler.setFormatter(self.__get_formatter(debug))
        self.logger.addHandler(file_handler)

        # Add console handler for immediate output
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(self.__get_formatter(debug))
        self.logger.addHandler(console_handler)

    def __get_formatter(self, debug: bool) -> logging.Formatter:
        """
        Return a formatter based on debug mode.

        Args:
            debug: If True, include detailed fields in log format.

        Returns:
            Configured logging.Formatter instance.   
        """

        fmt = (
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)d"
            if debug
            else "%(asctime)s - %(levelname)s - %(message)s"
        )
        return logging.Formatter(fmt)
    
    def debug(self, msg: str) -> None:
        """Log a debug message.

        Args:
            msg: Message to log.
        """
        self.logger.debug(msg)

    def info(self, msg: str) -> None:
        """Log an info message.

        Args:
            msg: Message to log.
        """
        self.logger.info(msg)

    def warning(self, msg: str) -> None:
        """Log a warning message.

        Args:
            msg: Message to log.
        """
        self.logger.warning(msg)

    def error(self, msg: str) -> None:
        """Log an error message.

        Args:
            msg: Message to log.
        """
        self.logger.error(msg)

    def critical(self, msg: str) -> None:
        """Log a critical message.

        Args:
            msg: Message to log.
        """
        self.logger.critical(msg)