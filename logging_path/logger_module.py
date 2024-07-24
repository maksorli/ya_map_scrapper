import logging
from typing import Optional

class LoggerSetup:
    def __init__(self, name: str, log_path: str = "logging_path/app.log") -> None:
        """
        Initialize the LoggerSetup with a logger name and log file path.

        Args:
            name (str): Name of the logger.
            log_path (str): Path to the log file. Defaults to "logging_path/app.log".
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)  # Set logging level
        self.configure(log_path)

    def configure(self, log_path: str) -> None:
        """
        Configure the logger with a file handler and a stream handler.

        Args:
            log_path (str): Path to the log file.
        """
        # File handler configuration
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(logging.DEBUG)  # Set logging level for file handler
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )

        # Stream handler configuration
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)  # Set logging level for stream handler
        stream_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )

        # Add handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)

    def get_logger(self) -> logging.Logger:
        """
        Get the configured logger.

        Returns:
            logging.Logger: The configured logger instance.
        """
        return self.logger
