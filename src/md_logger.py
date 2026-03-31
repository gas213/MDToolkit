import logging
import logging.handlers
import os.path
import sys

class MDLogger:
    FORMATTER = logging.Formatter("%(asctime)s - %(message)s")
    LOGGER_NAME: str = "main"

    def __init__(self):
        self.logger = logging.getLogger(self.LOGGER_NAME)
        self.logger.setLevel(logging.DEBUG)

        sysout_handler = logging.StreamHandler(sys.stdout)
        sysout_handler.setLevel(logging.DEBUG)
        sysout_handler.setFormatter(self.FORMATTER)
        self.logger.addHandler(sysout_handler)

        self.mem_handler = logging.handlers.MemoryHandler(capacity=1024)
        self.mem_handler.setLevel(logging.DEBUG)
        self.mem_handler.setFormatter(self.FORMATTER)
        self.logger.addHandler(self.mem_handler)

    def set_file_handler(self, path: str):
        file_handler = logging.FileHandler(os.path.join(path, "log.txt"))
        file_handler.setFormatter(self.FORMATTER)
        self.logger.addHandler(file_handler)
        self.mem_handler.setTarget(file_handler)
        self.mem_handler.flush()
        self.logger.removeHandler(self.mem_handler)

    def log(self, message: str):
        self.logger.debug(message)