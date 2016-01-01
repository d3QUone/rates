__author__ = 'vladimir'

import os
import sys
from uuid import uuid4
import logging
from logging import DEBUG, INFO, ERROR


reload(sys)
sys.setdefaultencoding("utf8")


class Logger(object):
    DEFAULT_FORMAT = "%(asctime)s | %(levelname)s | %(message)s"
    DEFAULT_LEVEL = INFO
    BASE_DIR = "log"

    def __init__(self, name):
        self.logger_id = str(uuid4())
        if not os.path.isdir(self.BASE_DIR):
            os.mkdir(self.BASE_DIR)
        self.filename = os.path.join(self.BASE_DIR, "{}.log".format(name))

        self.formatter = logging.Formatter(self.DEFAULT_FORMAT)
        self.syslog = logging.StreamHandler(sys.stdout)
        self.syslog.setFormatter(self.formatter)
        self.syslog.setLevel(self.DEFAULT_LEVEL)
        self.file_handler = logging.FileHandler(self.filename, encoding="utf8")
        self.file_handler.setFormatter(self.formatter)
        self.file_handler.setLevel(self.DEFAULT_LEVEL)
        self.logger = logging.getLogger("{}-{}".format(self.logger_id, self.filename))
        self.logger.setLevel(self.DEFAULT_LEVEL)
        self.logger.addHandler(self.syslog)
        self.logger.addHandler(self.file_handler)

    def info(self, msg, extra=None):
        self.logger.info(msg, extra=extra)

    def error(self, msg, extra=None):
        self.logger.error(msg, extra=extra)

    def debug(self, msg, extra=None):
        self.logger.debug(msg, extra=extra)

    def warn(self, msg, extra=None):
        self.logger.warn(msg, extra=extra)
