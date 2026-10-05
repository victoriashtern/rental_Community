import logging
import os

class AppLogger:
    def __init__(self, name="AppLogger", log_file="app.log", level=logging.INFO):
        """
        Initializes the logger with console and file output handlers.
        
        :param name: Name of the logger (default: 'AppLogger')
        :param log_file: Path to the log file (default: 'app.log')
        :param level: Logging level (e.g., logging.INFO, logging.DEBUG)
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Prevent adding duplicate handlers if the class is instantiated multiple times
        if not self.logger.handlers:
            # Define standard log format
            formatter = logging.Formatter(
                fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            
            # # 1. Console Handler (stdout)
            # console_handler = logging.StreamHandler()
            # console_handler.setFormatter(formatter)
            # self.logger.addHandler(console_handler)
            
            # 2. File Handler
            if log_file:
                file_handler = logging.FileHandler(log_file, encoding="utf-8")
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message, exc_info=False):
        # Pass exc_info=True if you want to log the stack trace along with the error
        self.logger.error(message, exc_info=exc_info)

    def debug(self, message):
        self.logger.debug(message)

    def critical(self, message, exc_info=True):
        self.logger.critical(message, exc_info=exc_info)