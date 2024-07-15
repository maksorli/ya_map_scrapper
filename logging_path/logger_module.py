import logging

class LoggerSetup:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        self.configure()

    def configure(self):
        file_handler = logging.FileHandler("logging_path/app.log")
        file_handler.setFormatter(logging.Formatter("%(name)s - %(levelname)s - %(message)s"))
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter("%(name)s - %(levelname)s - %(message)s"))
        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)