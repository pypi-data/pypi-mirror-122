import logging
import multiprocessing
import os

__all__ = [
    "get_prefixed_logger",
    "get_file_handler"
]


class LockingFileHandler(logging.FileHandler):
    def __init__(self, filename):
        super().__init__(filename)

    def emit(self, record: logging.LogRecord) -> None:
        with multiprocessing.Lock():
            super().emit(record)


def get_prefixed_logger(parent_logger, prefix) -> logging.Logger:
    class CustomAdapter(logging.LoggerAdapter):
        def process(self, msg, kwargs):
            return '%s %s' % (self.extra['prefix'], msg), kwargs

    return CustomAdapter(parent_logger, {'prefix': prefix})


def get_file_handler(path: str,
                     fmt: str = "%(asctime)s %(levelname)-5s %(funcName)-26s %(message)s",
                     datefmt: str = "%Y-%m-%d %H:%M:%S",
                     multiprocessing_safe=False) -> logging.FileHandler:
    assert os.path.exists(path)

    formatter = logging.Formatter(fmt)
    formatter.datefmt = datefmt

    cls = LockingFileHandler if multiprocessing_safe else logging.FileHandler
    handler = cls(path)
    handler.setFormatter(formatter)
    return handler
